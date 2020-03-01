from flask import Blueprint
import os

osenv = Blueprint("osenv", __name__, static_folder='static')

@osenv.route('')
def printos():
    try:
        os_env = {}
        os_env['AWS_DB_HOST'] = os.getenv('AWS_DB_HOST')
        os_env['AWS_DB_USERNAME'] = os.getenv('AWS_DB_USERNAME')
        os_env['AWS_DB_PASSWORD'] = os.getenv('AWS_DB_PASSWORD')
        os_env['AWS_DB_DEFAULT'] = os.getenv('AWS_DB_DEFAULT')
        return os_env
    except Exception as e:
        return str(e)
