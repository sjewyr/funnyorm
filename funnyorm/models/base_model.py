from funnyorm.models.exceptions import (
    FuckMeWhyNoDefaultIsProvidedWhenValueIsNotSetException,
    MultiplePrimaryKeysException)
from funnyorm.models.fields import Field, IntegerField
from funnyorm.models.supported_databases import SUPPORTED_DATABASES


class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        # Инициализация нового класса
        fields = {}
        lookup_field_name = dct.get("lookup_field", "id")
        cnt = 0

        # Сборка всех полей Field
        for key, val in dct.items():
            if isinstance(val, Field):
                fields[key] = val
                if val.pk:
                    if cnt:
                        raise MultiplePrimaryKeysException(name)
                    cnt = 1

        # Если lookup_field отсутствует в полях, добавляем его
        if lookup_field_name not in fields:
            fields[lookup_field_name] = IntegerField(nullable=True, auto=True)

        # Установка table_name на уровне класса
        dct["table_name"] = name

        dct["fields"] = fields
        return super().__new__(cls, name, bases, dct)


class BaseModel(metaclass=ModelMeta):
    database = None
    lookup_field = "id"
    fields: dict[str, Field] = {}

    def __init__(self, **kwargs):
        for key, val in self.fields.items():
            value = kwargs.get(key, val.default)
            val.value = value

    @classmethod
    def register_database(cls, database):
        cls.database = database
        for _, field in cls.fields.items():
            field.db_type = database.get_db_type()

    def save(self):
        if not self.fields.get(self.lookup_field)._db_value:
            self.__full_update()
            self.database.driver.insert(
                self.table_name,
                {k: v.value for k, v in self.fields.items() if not v.auto},
            )
            return
        to_update = {}
        for k, v in self.fields.items():
            if v.value != v._db_value and not v.auto:
                to_update[k] = v.value
                v._update()

        self.database.driver.update(
            self.table_name,
            to_update,
            f"{self.lookup_field}={self.fields.get(self.lookup_field).value}",
        )

    def __getattribute__(self, name):
        fields = super().__getattribute__("fields")
        if name in fields:
            return fields[name].value
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name in self.fields:
            self.fields[name].value = value
        else:
            super().__setattr__(name, value)

    def __full_update(self):
        for k, v in self.fields.items():
            if (
                v.value is None
                and not v.nullable
                and not (isinstance(v, IntegerField) and v.auto)
            ):
                raise FuckMeWhyNoDefaultIsProvidedWhenValueIsNotSetException(k)
            v._update()

    @classmethod
    def get(cls, lookup_value):
        """Get object by primary key"""
        if not hasattr(cls, "database"):
            raise Exception("Database is not initialized")

        try:
            res = cls.database.driver.get(
                cls.__name__,
                [k for k in cls.fields.keys()],
                f"{cls.lookup_field}={lookup_value}",
            )[0]
        except IndexError:
            return None

        obj = cls(**res)
        obj.__full_update()

        return obj

    @classmethod
    def make_creation_script(cls):
        """Make creation script for table"""
        result = []
        result.append("CREATE TABLE")
        if cls.database.driver.get_db_type() != SUPPORTED_DATABASES.FIREBIRD:
            result.append("IF NOT EXISTS")
        result.append(
            f"{cls.__name__} ("
            + ", ".join([f"{k} {v._to_create_code()}" for k, v in cls.fields.items()])
            + ");"
        )
        return " ".join(result)
