from funnyorm import models
from funnyorm.database.database import Database
from funnyorm.drivers import firebird_driver


class Fucker(models.base_model.BaseModel):
    id = models.fields.IntegerField(auto=True, primary_key=True)
    name = models.fields.CharField(max_length=255)


database = Database(
    firebird_driver.FirebirdDriver("127.0.0.1", 5432, "SYSDBA", "masterkey", "sex")
)

database.register_models(Fucker)

del database
user = Fucker(name="John Doe")
user.save()
