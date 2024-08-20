from abc import ABC, abstractmethod


class Driver(ABC):
    @abstractmethod
    def get(self, table, columns, condition: dict[str, str] = None):
        if not condition:
            query = f"SELECT {', '.join(columns)} FROM {table}"
        else:
            query = f"SELECT {', '.join(columns)} FROM {table} WHERE {condition}"
        self.execute(query)

    @abstractmethod
    def insert(self, table, data):
        keys = ", ".join(data.keys())
        values = ", ".join([f"'{_}'" for _ in data.values()])
        query = f"INSERT INTO {table} ({keys}) VALUES ({values})"
        return self.execute(query, data)

    @abstractmethod
    def update(self, table, data, condition):
        set_values = ", ".join([f"{key}='{value}'" for key, value in data.items()])
        query = f"UPDATE {table} SET {set_values} WHERE {condition}"
        return self.execute(query)

    @abstractmethod
    def get_db_type(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self, query, params=None):
        raise NotImplementedError
