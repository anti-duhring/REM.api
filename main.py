from flask import Flask, make_response, jsonify, request
from controllers.user import UserController

app = Flask('RemAPI')
app.config['JSON_SORT_KEYS'] = False

@app.route('/users', methods=['GET'])
def show():
    user_id = request.args.get('id')

    try:
        if user_id:
            result = UserController().show(user_id=user_id)
        else:
            result = UserController().index()
        return result
    except Exception as e:
        print(e)
        return make_response({
            'message': 'Erro interno'
        }, 500)

@app.route('/users', methods=['POST'])
def create():
    request_data = request.get_json()

    try:
        result = UserController().create(data=request_data)
        return result
    except Exception as e:
        print(e)
        return make_response({
            'message': 'Erro interno'
        }, 500)    

@app.route('/users', methods=['DELETE'])
def delete():
    user_id = request.args.get('id')

    try:
        result = UserController().delete(user_id=user_id)
        return result
    except Exception as e:
        print(e)
        return make_response({
            'message': 'Erro interno'
        }, 500)

@app.route('/users', methods=['PUT'])
def update():
    user_id = request.args.get('id')
    request_data = request.get_json()

    try:
        result = UserController().update(user_id=user_id, data=request_data)
        return result
    except Exception as e:
        print(e)
        return make_response({
            'message': 'Erro interno'
        }, 500) 

# app.run(debug=True)
app.run()