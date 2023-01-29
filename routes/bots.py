from flask import make_response, request

from __main__ import app
from controllers.bot import BotController
from views import helper


@app.route('/bots/download', methods=['POST'])
@helper.access_required
def download_bots(user):
  request_data = request.get_json()
  try:
    response = BotController().download(request_data=request_data)
    return make_response(response, 200)
  except Exception as e:
    return make_response({'message': 'Erro interno'}, 500)


@app.route('/bots', methods=['GET'])
def show_bots():
  bot_id = request.args.get('id')

  try:
    if bot_id:
      result = BotController().show(bot_id=bot_id)
    else:
      result = BotController().index()

    if result['error'] == True:
      return make_response({'message': result['message']}, 401)

    return make_response(result, 200)
  except Exception as e:

    print(e)
    return make_response({'message': 'Erro interno'}, 500)


@app.route('/bots', methods=['POST'])
@helper.admin_required
def create_bots():
  request_data = request.get_json()

  try:
    result = BotController().create(data=request_data)

    if result['error']:
      return make_response({'message': result['message']}, 401)

    return make_response(result, 201)
  except Exception as e:
    print(e)
    return make_response({'message': 'Erro interno'}, 500)


@app.route('/bots', methods=['DELETE'])
@helper.admin_required
def delete_bots():
  bot_id = request.args.get('id')

  try:
    result = BotController().delete(bot_id=bot_id)

    if result['error']:
      return make_response({'message': result['message']}, 401)

    return make_response(result, 200)
  except Exception as e:
    print(e)
    return make_response({'message': 'Erro interno'}, 500)


@app.route('/bots', methods=['PUT'])
@helper.admin_required
def update_bots():
  bot_id = request.args.get('id')
  request_data = request.get_json()

  try:
    result = BotController().update(bot_id=bot_id, data=request_data)

    if result['error']:
      return make_response({'message': result['message']}, 401)

    return make_response(result, 201)
  except Exception as e:
    print(e)
    return make_response({'message': 'Erro interno'}, 500)
