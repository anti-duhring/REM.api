from db import ConnectDB
import json
import collections

class UserController:
    def __init__(self):
        print('Initialize user controller')

    def create(self, data):
        ConnectDB().connect()
        res = {}

        token = data['token']
        admin = data['admin']
        access = data['access']
        name = data['name']

        command = f'INSERT INTO Users (token, admin, access, name) VALUES ("{token}", {admin}, {access}, "{name}")'

        try:
            ConnectDB().exec_DML(sql=command)
            res['user'] = self.show_by_token(token=token)
        except Exception as e:
            print(e)
            res['message'] = 'Erro ao criar usuário usuário'

        return res
    
    def index(self):
        ConnectDB().connect()
        users_list = {}
        users_list["users"] = []

        command = f'''SELECT 
            id, 
            token, 
            name,
            admin,
            access 
        FROM Users'''

        result = ConnectDB().exec_DQL(sql=command)
        for row in result:
            d = collections.OrderedDict()
            d["id"] = row[0]
            d["token"] = row[1]
            d["name"] = row[2]
            d["admin"] = row[3]
            d["access"] = row[4]
            users_list["users"].append(d)

        return users_list
        
    def show(self, user_id):
        ConnectDB().connect()
        user = {}
        command = f'''SELECT 
            id, 
            token, 
            name,
            admin,
            access 
        FROM Users WHERE id = {user_id}'''


        result = ConnectDB().exec_DQL(sql=command)
        for row in result:
            user["id"] = row[0]
            user["token"] = row[1]
            user["name"] = row[2]
            user["admin"] = row[3]
            user["access"] = row[4]

        return user

    def show_by_token(self, token):
        ConnectDB().connect()
        user = {}
        command = f'''SELECT 
            id, 
            token, 
            name,
            admin,
            access 
        FROM Users WHERE token = {token}'''


        result = ConnectDB().exec_DQL(sql=command)
        for row in result:
            user["id"] = row[0]
            user["token"] = row[1]
            user["name"] = row[2]
            user["admin"] = row[3]
            user["access"] = row[4]

        return user     

    def update(self, user_id, data):
        ConnectDB().connect()
        res = {}
        admin = data['admin']
        access = data['access']
        name = data['name']

        command = f'UPDATE Users SET name = "{name}", access = {access}, admin = {admin} WHERE id = {user_id}'

        try:
            ConnectDB().exec_DML(sql=command)
            res['user'] = self.show(user_id=user_id)
        except Exception as e:
            print(e)
            res['message'] = 'Erro ao criar usuário usuário'

        return res
    
    def delete(self, user_id):
        ConnectDB().connect()
        res = {
            "message": f'Usuário {user_id} deletado com sucesso'
        }
        command = f'DELETE FROM Users WHERE id = {user_id}'
        
        try:
            ConnectDB().exec_DML(sql=command)
        except Exception as e:
            print(e)
            res['message'] = 'Erro ao deletar usuário'

        return res
        