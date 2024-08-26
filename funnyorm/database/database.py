from typing import Any

from funnyorm.common.driver import Driver


class Database:
    def __init__(self, driver: Driver, *args, **kwargs):
        self.driver = driver
        self.models: list[Any] = []

    def register_models(self, *models):
        for model in models:
            model.register_database(self)

            self.models.append(model)

    def create_models(self):
        for model in self.models:
            self.driver.create_model(model)

    def get_db_type(self):
        return self.driver.get_db_type()

    def __del__(self):
        self.driver.__del__()
