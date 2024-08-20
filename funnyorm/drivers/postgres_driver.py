import psycopg
import psycopg.rows
import psycopg_pool

from funnyorm.common.driver import Driver
from funnyorm.models.supported_databases import SUPPORTED_DATABASES


class PostgresDriver(Driver):
    def __init__(self, host, port, user, password, dbname):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.initial_connect()

    @staticmethod
    def get_driver_name():
        return "Postgres"

    def initial_connect(self):
        self.connection_pool = psycopg_pool.ConnectionPool(
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}",
            open=True,
        )
        with self.connection_pool.connection() as conn:
            conn.cursor()

    def get(self, table, columns, condition: dict[str, str] = None):
        if not condition:
            query = f"SELECT {', '.join(columns)} FROM {table}"
        else:
            query = f"SELECT {', '.join(columns)} FROM {table} WHERE {condition}"
        with self.connection_pool.connection() as conn:
            with conn.cursor(binary=False, row_factory=psycopg.rows.dict_row) as cur:
                print(query)
                res = cur.execute(query)
                return res.fetchall()

    def insert(self, table, data):
        column_names = ", ".join(data.keys())
        placeholder_values = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholder_values})"
        with self.connection_pool.connection() as conn:
            with conn.cursor() as cur:
                print(query)
                cur.execute(query, tuple(data.values()))
                conn.commit()

    def update(self, table, data, condition):
        set_values = ", ".join([f"{key}=%s" for key in data.keys()])
        query = f"UPDATE {table} SET {set_values} WHERE {condition}"
        with self.connection_pool.connection() as conn:
            with conn.cursor() as cur:
                print(query)
                cur.execute(query, tuple(data.values()))
                conn.commit()

    def execute(self, query, params):
        with self.connection_pool.connection() as conn:
            with conn.cursor() as cur:
                print(query)
                cur.execute(query, params)
                conn.commit()

    def get_db_type(self):
        return SUPPORTED_DATABASES.POSTGRES
