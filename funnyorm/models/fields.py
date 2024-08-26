from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from funnyorm.models.base_model import BaseModel

from funnyorm.models.exceptions import UnsupportedDatabaseException
from funnyorm.models.supported_databases import SUPPORTED_DATABASES


class Field:
    db_type = None
    auto = False
    fk: BaseModel = None
    fk_to: str = None

    def __init__(self, nullable=False, primary_key=False):
        """
        Class for fields that should be used inside the models to represent columns in the database.
        :param nullable: Boolean indicating whether the field can be null.
        :param primary_key: Boolean indicating whether the field is a primary key.
        :param default: Optional default value for the field.
        :param fk: Optional foreign key associated model for the field (Should be a subclass of BaseModel)
        :param fk_to: Optional field name in the foreign key model to which the current field points.
        """
        self._db_value: Any = None
        self.nullable = nullable
        self.value: Any = None
        self.default: Any = None
        self.pk = primary_key

    def _update(self):
        raise NotImplementedError

    def _to_create_code():
        raise NotImplementedError

    def assert_database(self):
        try:
            assert self.db_type
            assert self.db_type in SUPPORTED_DATABASES
        except (AssertionError, TypeError):
            raise UnsupportedDatabaseException(self.db_type)


class IntegerField(Field):
    def __init__(
        self,
        nullable: bool = False,
        default: None | int = None,
        auto: bool = False,
        primary_key: bool = False,
        fk: BaseModel = None,
        fk_to: str = None,
    ):
        self._db_value = None
        self.nullable = nullable
        self.value = default
        self.default = default
        self.auto = auto
        self.pk = primary_key
        self.fk = fk
        self.fk_to = fk_to

    def _update(self):
        self._db_value = self.value

    def _to_create_code(self):
        try:
            assert self.db_type
        except AssertionError:
            raise ValueError(
                "Trying to create a new IntegerField on a model without a registered database"
            )
        res = []
        if self.auto and self.db_type == SUPPORTED_DATABASES.POSTGRES:
            res.append("SERIAL")
        else:
            res.append("INTEGER")

        if self.default is not None:
            res.append(f"DEFAULT {self.default}")
        if self.nullable:
            res.append("NOT NULL")
        if self.auto and self.db_type != SUPPORTED_DATABASES.POSTGRES:
            res.append("GENERATED BY DEFAULT AS IDENTITY")
        if self.pk:
            res.append("PRIMARY KEY")

        if self.fk:
            res.append(f"REFERENCES {self.fk.__name__}({self.fk_to})")

        return " ".join(res)


class CharField(Field):
    def __init__(
        self,
        max_length: int,
        nullable: bool = False,
        default: None | str = None,
        primary_key: bool = False,
        fk: BaseModel = None,
        fk_to: str = None,
    ):
        self._db_value = None
        self.nullable = nullable
        self.value = default
        self.default = default
        self.max_length = max_length
        self.pk = primary_key
        self.fk = fk
        self.fk_to = fk_to

    def _update(self):
        self._db_value = self.value

    def _to_create_code(self):
        self.assert_database()
        res = ["VARCHAR({})".format(self.max_length)]
        if self.default is not None:
            res.append(f"DEFAULT '{self.default}'")
        if self.nullable:
            res.append("NOT NULL")
        if self.pk:
            res.append("PRIMARY KEY")

        if self.fk:
            res.append(f"REFERENCES {self.fk.__class__.__name__}({self.fk_to})")

        return " ".join(res)
