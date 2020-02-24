from flask import Blueprint

home = Blueprint("home", __name__, static_folder='static')

@home.route('/')
def hello_world():
    return home.send_static_file('index.html')