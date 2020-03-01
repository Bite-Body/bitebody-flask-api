from flask import Blueprint
import os

osenv = Blueprint("osenv", __name__, static_folder='static')

@osenv.route('')
def printos():
    try:
        os_env = {}
        PATH = os.getenv('AWS_DB_HOST')
        os_env['AWS_DB_HOST'] = PATH
        return os_env
    except Exception as e:
        return str(e)
