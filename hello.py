from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<p>Hello User</p>"

@app.route('/user')
def user():
    return "<p>Hello User</p>"