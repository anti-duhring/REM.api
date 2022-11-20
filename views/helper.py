from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import jsonify, request

from controllers.user import UserController
from __main__ import app


def admin():
    auth = request.headers.get('token')

    if not auth:
        return jsonify({
            'message': 'Dados de autorização ausentes',
        }), 400
    
    user = UserController().show_by_token(token=auth, format='json')

    if not user:
        return jsonify({
            'message': 'Usuário não existe',
            'user': {}
        }), 404
    else:
        token = jwt.encode({
            'id': user.get('id'),
            'token': user.get('token'),
            'exp': datetime.now() + timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        if user.get('admin'):
            return jsonify({
                'message': 'Sucesso ao validar',
                'token': token,
                'exp': datetime.now() + timedelta(hours=24)
            }), 200
        else:
            return jsonify({
                    'message': 'Não autorizado',
            }), 403

    return jsonify({
            'message': 'Erro interno',
    }), 500

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return jsonify({
                'message': 'Token ausente'
            }),400
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = UserController().show_by_token(token=data.get('token'), format='json')
        except Exception as e:
            print(e)
            return jsonify({
                'message': 'Tokendf inválida ou expirada'
            }),401
        return f(*args, **kwargs)
    return decorated