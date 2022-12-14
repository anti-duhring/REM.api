from datetime import datetime, timedelta
from functools import wraps
from jwt import (
  JWT,
  jwk_from_dict,
  jwk_from_pem,
)
from jwt.utils import get_int_from_datetime
from flask import jsonify, request
from controllers.user import UserController
from __main__ import app


def token():
  jwt = JWT()
  auth = request.headers.get('token')

  if not auth:
    return jsonify({
      'message': 'Dados de autorização ausentes',
    }), 400

  user = UserController().show_by_token(token=auth, format='json')

  if not user:
    return jsonify({'message': 'Usuário não existe', 'user': {}}), 404
  else:
    last_login = UserController().update_last_login(user_id=user.get('id'))

    if last_login['error']:
      return jsonify({
        'message': last_login['message'],
      }), 500

    token = jwt.encode(
      {
        'id': user.get('id'),
        'token': user.get('token'),
        'exp': get_int_from_datetime(datetime.now() + timedelta(hours=24))
      }, jwk_from_dict(app.config['SECRET_KEY']))
    return jsonify({
      'message':
      'Sucesso ao validar',
      'user':
      user,
      'token':
      token,
      'exp':
      get_int_from_datetime(datetime.now() + timedelta(hours=24))
    }), 200

def access_required(f):

  @wraps(f)
  def decorated(*args, **kwargs):
    jwt = JWT()
    token = request.headers.get('token')
    if not token:
      return jsonify({'message': 'Token ausente'}), 400
    try:
      data = jwt.decode(
        token,
        jwk_from_dict(app.config['SECRET_KEY']),
        algorithms=['HS256']
      )
      current_user = UserController().show_by_token(
          token=data.get('token'),
          format='json'
        )
      if current_user.get('access') is False or current_user.get('access') == 0:
        return jsonify({'message': 'Acesso do usuário está bloqueado'}), 403
  
    except Exception as e:
      print(e)
      return jsonify({'message': 'Token inválida ou expirada'}), 401
    return f(user=current_user, *args, **kwargs)

  return decorated   

def admin_required(f):

  @wraps(f)
  def decorated(*args, **kwargs):
    jwt = JWT()
    token = request.headers.get('token')
    if not token:
      return jsonify({'message': 'Token ausente'}), 400
    try:
      data = jwt.decode(token,
                        jwk_from_dict(app.config['SECRET_KEY']),
                        algorithms=['HS256'])
      current_user = UserController().show_by_token(
        token=data.get('token'),
        format='json'
      )
      if current_user.get('admin') is False or current_user.get('admin') == 0:
        return jsonify({'message': 'Não autorizado'}), 403

    except Exception as e:
      print(e)
      return jsonify({'message': 'Token inválida ou expirada'}), 401
    return f(*args, **kwargs)

  return decorated 
