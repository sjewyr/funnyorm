from firebird.driver import (
    DatabaseError,
    connect,
    create_database,
    driver_config,
    types,
)

from funnyorm.common.driver import Driver
from funnyorm.drivers.exceptions import ForeignKeyViolationException
from funnyorm.models.supported_databases import SUPPORTED_DATABASES


class FirebirdDriver(Driver):
    def __init__(self, host, port, user, password, dbname):
        print("Херня этот ваш firebird_driver конечно")
        srv_cfg = f"""[{dbname}_server]
        host = {host}
        user = {user}
        password = {password}
        """
        driver_config.register_server(f"{dbname}_server", srv_cfg)

        # Register database
        db_cfg = f"""[{dbname}]
        server = {dbname}_server
        database = {dbname}.fdb
        protocol = inet
        charset = utf8
        """
        driver_config.register_database(dbname, db_cfg)
        try:
            self.con = create_database(dbname)
        except DatabaseError:
            self.con = connect(dbname)

    def __del__(self):
        try:
            self.con.close()
        except Exception:
            print(
                "Фаерберд ругается, грустно конечно но что поделаешь я и так отлавливаю соединение ну куда он почему"
            )

    def get_db_type(self):
        return SUPPORTED_DATABASES.FIREBIRD

    def execute(self, query, params=None):
        with self.con.cursor() as cursor:
            results = cursor.execute(query, params)
            res = None
            if results._result:
                res = results.fetchall()
            if results.description:
                res = results.description[0][2]
            self.con.commit()
            return res

    def get(self, table, columns, condition: dict[str, str] = None):
        return super().get(table, columns, condition)

    def insert(self, table, data, lookup_field):
        try:
            return super().insert(table, data, lookup_field)
        except types.DatabaseError as e:
            if "violation of foreign key" in str(e).lower():
                raise ForeignKeyViolationException(table)
            raise e

    def update(self, table, data, condition, lookup_field):
        return super().update(table, data, condition, lookup_field)

    def create_model(self, model):
        try:
            return super().create_model(model)
        except types.DatabaseError:
            pass
