from flask import Flask, Response, request

from web.db import db, User
from web.api import get_weather_in_city

from random import randint
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'

with app.app_context():
    db.init_app(app)
    db.create_all()
    if not len(User.get_users()):
        for i in range(1, 6):
            User.add_user(f'user{i}', randint(10000, 15000))

@app.get('/ping')
async def pingpong():
    return {'_': 'pong'}

@app.post('/user')
async def create_user():
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
async def update_user(user_id: int):
    city = request.args.get('city')
    if not city:
        return Response(json.dumps({
            'errors': [{'city': 'City must be provided!'}]
        }), status=422)

    try:
        user = User.change_balance(user_id, balance=await get_weather_in_city(city))
    except AssertionError as e:
        return Response(json.dumps({
            'errors': e.args
        }), status=409)    

    return Response(json.dumps(
        {'message': 'success'}
    ), status=200)