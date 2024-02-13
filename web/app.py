from flask import Flask, Response, request

import json

from web.db import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'

with app.app_context():
    db.init_app(app)
    db.create_all()

@app.get('/ping')
def pingpong():
    return {'_': 'pong'}

@app.post('/user')
def create_user():
    username = request.args['username']
    balance = int(request.args['balance'])

    try:
        db.session.add(User(username, balance))
        db.session.commit()
    except AssertionError as e:
        return Response(json.dumps({
            'errors': e.args
        }), status=422)    

    return Response(status=201)