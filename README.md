## FunnyORM

### Поддерживаемые типы данных
На данный момент orm умеет работать с Integer и Varchar, так же умеет использовать Foreign key

### Поддерживаемые базы данных
На данный момент orm умеет работать с Firebird (очень крутая база данных) и PostgreSQL

### Пример кода
```python

from funnyorm import models
from funnyorm.database.database import Database
from funnyorm.drivers import firebird_driver, postgres_driver

class Person(models.base_model.BaseModel):
    id = models.fields.IntegerField(auto=True, primary_key=True)
    name = models.fields.CharField(max_length=255)


class Child(models.base_model.BaseModel):
    id = models.fields.IntegerField(auto=True, primary_key=True)
    name = models.fields.CharField(max_length=255)
    raised_by = models.fields.IntegerField(fk=Person, fk_to="id")

postgres_test = postgres_driver.PostgresDriver(
    "127.0.0.1", 5432, "login", "password", "dbname"
)

database = Database(postgres_test)


database.register_models(Person, Child) # Register the models for the database
database.create_models() # Creating tables for each model
user = Person(name=1) # Create a new Person object
child = Child(name=2, raised_by=25) # Create a new Child object with a fk to a user
print(user.id) # None
user.save()
print(user.id) # 1
```
