from flask import Flask, make_response, jsonify, request
from controllers.user import UserController

app = Flask('RemAPI')

@app.route('/users', methods=['GET'])
def show():
    user_id = request.args.get('id')

    try:
        if user_id:
            result = UserController().show(user_id=user_id)
        else:
            result = UserController().index()
        return make_response(
            result
        )
    except Exception as e:
        print(e)
        return make_response({
            'message': 'Erro interno'
        })

@app.route('/users', methods=['POST'])
def create():
    request_data = request.get_json()

    try:
        result = UserController().create(data=request_data)
        return make_response(
            result
        )
    except Exception as e:
        print(e)
        return make_response({
            'message': 'Erro interno'
        })    

@app.route('/users', methods=['DELETE'])
def delete():
    user_id = request.args.get('id')

    try:
        result = UserController().delete(user_id=user_id)
        return make_response(
            result
        )
    except Exception as e:
        print(e)
        return make_response({
            'message': 'Erro interno'
        })

@app.route('/users', methods=['PUT'])
def update():
    user_id = request.args.get('id')
    request_data = request.get_json()

    try:
        result = UserController().update(user_id=user_id, data=request_data)
        return make_response(
            result
        )
    except Exception as e:
        print(e)
        return make_response({
            'message': 'Erro interno'
        }) 

app.run()