from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'

@app.get('/ping')
def pingpong():
    return {'_': 'pong'}