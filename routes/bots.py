from flask import make_response, request

from __main__ import app
from controllers.bot import BotController
from views import helper

@app.route('/bots/download', methods=['POST'])
@helper.access_required
def download(user):
    try:
        response = BotController().download()
        return make_response(response, 200)
    except Exception as e:
        return make_response({'message': 'Erro interno'}, 500)