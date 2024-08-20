from firebird.driver import (DatabaseError, connect, create_database,
                             driver_config)

from funnyorm.common.driver import Driver
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
            self.con.commit()
            if results.rowcount > 0:
                return results.fetchall()
            return

    def get(self, table, columns, condition: dict[str, str] = None):
        return super().get(table, columns, condition)

    def insert(self, table, data):
        super().insert(table, data)

    def update(self, table, data, condition):
        return super().update(table, data, condition)
