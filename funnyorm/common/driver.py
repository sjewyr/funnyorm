from abc import ABC, abstractmethod


class Driver(ABC):
    @abstractmethod
    def create_model(self, model):
        self.execute(model.make_creation_script())

    @abstractmethod
    def get(self, table, columns, condition: dict[str, str] = None):
        if not condition:
            query = f"SELECT {', '.join(columns)} FROM {table}"
        else:
            query = f"SELECT {', '.join(columns)} FROM {table} WHERE {condition}"

        print(query)
        return self.execute(query)

    @abstractmethod
    def insert(self, table, data, lookup_field):
        keys = ", ".join(data.keys())
        values = ", ".join([f"'{_}'" for _ in data.values()])
        query = (
            f"INSERT INTO {table} ({keys}) VALUES ({values}) RETURNING {lookup_field}"
        )
        return self.execute(query, data)

    @abstractmethod
    def update(self, table, data, condition, lookup_field):
        set_values = ", ".join([f"{key}='{value}'" for key, value in data.items()])
        query = f"UPDATE {table} SET {set_values} WHERE {condition} RETURNING {lookup_field}"
        return self.execute(query)

    @abstractmethod
    def get_db_type(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self, query, params=None):
        raise NotImplementedError
