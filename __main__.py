from flask import Flask
from waitress import serve
import json
from config.secret_key import key

app = Flask('RemAPI')
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = key


@app.after_request
def apply_caching(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Methods',
                       'GET,POST,OPTIONS,DELETE,PUT')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type, token')
  return response


from routes import users, bots

app.run(debug=True,port=8080)
# serve(app, host="0.0.0.0", port=8080)
