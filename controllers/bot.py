import requests
from requests.auth import HTTPBasicAuth

class BotController:

    def __init__(self):
        print('Initialize bot controller')

    def download(self, link = 'test.py'):
        res = {
            'content': None,
            'message': None,
            'error': False
        }
        response = requests.get(
            f'https://www.reminfotech.net.br/bots/{link}', 
            allow_redirects=True,
            auth=HTTPBasicAuth('reminfotech', 'a1b2c3d4e5')
        )
        if response.status_code == 200:
            res['content'] = response.content.decode('UTF-8')
        else:
            res['message'] = 'Erro ao baixar arquivo do bot'
            res['error'] = True
        
        return res