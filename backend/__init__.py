from db import connect_mysql
from controllers.user import UserController

@connect_mysql
def create(cursor, connection):
    data = {
        "token": "a2b3c4d5e6",
        "admin": 1,
        "access": 1,
        "name": "Mateus"
    }
    UserController(cursor=cursor, connection=connection).create(data=data)

@connect_mysql
def read(cursor, connection):
    data = {
        "token": "a1b2c3d4e5",
        "admin": 1,
        "access": 1,
        "name": "Teste"
    }
    users = UserController(cursor=cursor, connection=connection).read(data=data)
    print(users)

@connect_mysql
def update(cursor, connection):
    data = {
        "token": "a1b2c3d4e5",
        "admin": 1,
        "access": 1,
        "name": "Teste editado",
        "id": 1
    }
    UserController(cursor=cursor, connection=connection).update(data=data)

@connect_mysql
def delete(cursor, connection):
    data = {
        "id": 3
    }
    UserController(cursor=cursor, connection=connection).delete(data=data)

read()