import requests
from requests.auth import HTTPBasicAuth
from db import ConnectDB
import collections


class BotController:

  def __init__(self):
    print('Initialize bot controller')

  def download(self, link='test.py'):
    res = {'content': None, 'message': None, 'error': False}
    response = requests.get(f'https://www.reminfotech.net.br/bots/{link}',
                            allow_redirects=True,
                            auth=HTTPBasicAuth('reminfotech', 'a1b2c3d4e5'))
    if response.status_code == 200:
      res['content'] = response.content.decode('UTF-8')
    else:
      res['message'] = 'Erro ao baixar arquivo do bot'
      res['error'] = True

    return res

  def create(self, data):
    ConnectDB().connect()
    res = {'error': False}

    title = data['title']
    description = data['description']
    type = data['type']
    plataform = data['plataform']
    link = data['link']

    command = f'INSERT INTO bots (title, description, type, plataform, link) VALUES ("{title}", "{description}", "{type}", "{plataform}", "{link}")'

    try:
      ConnectDB().exec_DML(sql=command)
      res['bot'] = self.show(bot_link=link)

      return res
    except Exception as e:
      print(e)
      res['error'] = True
      res['message'] = 'Erro ao criar bot'
      return res

  def show(self, bot_id=None, bot_link=None):
    ConnectDB().connect()
    res = {
      'error': False,
    }

    if bot_id is not None:
      query = f'id = {bot_id}'
    else:
      query = f'link = "{bot_link}"'

    command = f'''SELECT 
                id, 
                title, 
                description,
                type,
                plataform,
                link 
            FROM bots WHERE {query}'''

    try:
      result = ConnectDB().exec_DQL(sql=command)
      res['bot'] = {}
      for row in result:
        res['bot']["id"] = row[0]
        res['bot']["title"] = row[1]
        res['bot']["description"] = row[2]
        res['bot']["type"] = row[3]
        res['bot']["plataform"] = row[4]
        res['bot']["link"] = row[5]

      return res
    except Exception as e:
      print(e)
      res['error'] = True
      res['message'] = 'Erro ao retornar bot'

      return res

  def index(self):
    ConnectDB().connect()
    res = {'error': False}

    command = f'''SELECT 
                id, 
                title, 
                description,
                type,
                plataform,
                link 
            FROM bots'''

    try:
      result = ConnectDB().exec_DQL(sql=command)
      res["bots"] = []
      for row in result:
        d = collections.OrderedDict()
        d["id"] = row[0]
        d["title"] = row[1]
        d["description"] = row[2]
        d["type"] = row[3]
        d["plataform"] = row[4]
        d["link"] = row[5]
        res["bots"].append(d)

      return res
    except Exception as e:
      print(e)
      res['error'] = True
      res['message'] = 'Erro ao retornar bots'

      return res

  def update(self, data, bot_id):
    ConnectDB().connect()
    res = {'error': False}

    title = data['title']
    description = data['description']
    type = data['type']
    plataform = data['plataform']
    link = data['link']

    command = f'UPDATE bots SET title = "{title}", description = "{description}", type = "{type}", plataform = "{plataform}", link = "{link}" WHERE id = {bot_id}'

    try:
      ConnectDB().exec_DML(sql=command)

      bot_updated = self.show(bot_id=bot_id)
      res['bot'] = bot_updated['bot']

      return res
    except Exception as e:
      print(e)
      res['error'] = True
      res['message'] = 'Erro ao criar bot'

      return res

  def delete(self, bot_id):
    ConnectDB().connect()
    res = {'error': False}
    command = f'DELETE FROM bots WHERE id = {bot_id}'

    try:
      ConnectDB().exec_DML(sql=command)

      res["message"] = f'Bot {bot_id} deletado com sucesso'
      return res
    except Exception as e:
      print(e)
      res['error'] = True
      res['message'] = 'Erro ao deletar bot'

      return res
