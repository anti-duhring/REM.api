import collections
import json
import random
import string
from flask import make_response
from db import ConnectDB
from datetime import datetime


class UserController:

  def __init__(self):
    print('Initialize user controller')

  def create(self, data, current_user=None):
    ConnectDB().connect()
    res = {}
    token = self.generate_token()
    admin = data['admin']
    access = data['access']
    name = data['name']

    command = f'INSERT INTO Users (token, admin, access, name) VALUES ("{token}", {admin}, {access}, "{name}")'

    try:
      ConnectDB().exec_DML(sql=command)
      res['user'] = self.show_by_token(token=token, format='json')

      return make_response(res, 201)
    except Exception as e:
      print(e)
      res['message'] = 'Erro ao criar usuário usuário'
      return make_response(res, 401)

  def index(self, format = 'response'):
    ConnectDB().connect()
    res = {}

    command = f'''SELECT 
            id, 
            token, 
            name,
            admin,
            access 
        FROM Users'''

    try:
      result = ConnectDB().exec_DQL(sql=command)
      res["users"] = []
      for row in result:
        d = collections.OrderedDict()
        d["id"] = row[0]
        d["token"] = row[1]
        d["name"] = row[2]
        d["admin"] = row[3]
        d["access"] = row[4]
        res["users"].append(d)

      if format == 'json':
        return res['users']
      else:
        return make_response(res, 200)
    except Exception as e:
      print(e)
      res['message'] = 'Erro ao retornar usuários'
      return make_response(res, 400)

  def show(self, user_id, format='response'):
    ConnectDB().connect()
    res = {}
    command = f'''SELECT 
            id, 
            token, 
            name,
            admin,
            access 
        FROM Users WHERE id = {user_id}'''

    try:
      result = ConnectDB().exec_DQL(sql=command)
      res['user'] = {}
      for row in result:
        res['user']["id"] = row[0]
        res['user']["token"] = row[1]
        res['user']["name"] = row[2]
        res['user']["admin"] = row[3]
        res['user']["access"] = row[4]

      if format == 'json':
        return res['user']
      else:
        return make_response(res, 200)
    except Exception as e:
      print(e)
      res['message'] = 'Erro ao retornar usuários'
      return make_response(res, 400)

  def show_by_token(self, token, format='response'):
    ConnectDB().connect()
    res = {}
    command = f'''SELECT 
            id, 
            token, 
            name,
            admin,
            access 
        FROM Users WHERE token = "{token}"'''

    try:
      result = ConnectDB().exec_DQL(sql=command)
      res['user'] = {}
      for row in result:
        res['user']["id"] = row[0]
        res['user']["token"] = row[1]
        res['user']["name"] = row[2]
        res['user']["admin"] = row[3]
        res['user']["access"] = row[4]

      if format == 'json':
        return res['user']
      else:
        return make_response(res, 200)
    except Exception as e:
      print(e)
      res['message'] = 'Erro ao retornar usuários'
      return make_response(res, 400)

  def update(self, user_id, data, current_user=None):
    ConnectDB().connect()
    res = {}
    admin = data['admin']
    access = data['access']
    name = data['name']

    command = f'UPDATE Users SET name = "{name}", access = {access}, admin = {admin} WHERE id = {user_id}'

    try:
      ConnectDB().exec_DML(sql=command)
      res['user'] = self.show(user_id=user_id, format='json')

      return make_response(res, 201)
    except Exception as e:
      print(e)
      res['message'] = 'Erro ao criar usuário usuário'
      return make_response(res, 400)

  def delete(self, user_id, current_user=None):
    ConnectDB().connect()
    res = {"message": f'Usuário {user_id} deletado com sucesso'}
    command = f'DELETE FROM Users WHERE id = {user_id}'

    try:
      ConnectDB().exec_DML(sql=command)

      return make_response(res, 200)
    except Exception as e:
      print(e)
      res['message'] = 'Erro ao deletar usuário'

      return make_response(res, 400)
  
  def update_last_login(self, user_id):
    ConnectDB().connect()
    res = {
      'message': None,
      'error': False
    }
    date_now = f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}'

    command = f'UPDATE Users SET lastLogin = "{date_now}" WHERE id = {user_id}'

    try:
      ConnectDB().exec_DML(sql=command)
      res['message'] = f'Último login em {date_now}'

      return res
    except Exception as e:
      print(e)
      res['message'] = 'Erro ao atualizar data do último login do usuário'
      res['error'] =  True

      return res 

  def generate_token(self):
    token = None
    users = self.index(format='json')

    def random_carac():
      carac = string.hexdigits
      result_str = ''.join(random.choice(carac) for i in range(10))
      for user in users:
        if result_str == user.get('token'):
          random_carac()
        else:
          return result_str
    
    token = random_carac()
    return token
