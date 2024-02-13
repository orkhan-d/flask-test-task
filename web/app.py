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
        User.add_user(username, balance)
    except AssertionError as e:
        return Response(json.dumps({
            'errors': e.args
        }), status=422)    

    return Response(status=201)


@app.put('/user/<user_id>')
def update_user(user_id: int):
    username = request.args.get('username')
    balance = request.args.get('balance')
    balance = int(balance) if balance else None

    try:
        user = User.update_user(user_id, username=username, balance=balance)
    except AssertionError as e:
        return Response(json.dumps({
            'errors': e.args
        }), status=422)    

    return Response(json.dumps(
        {'message': 'success'}
    ), status=200)