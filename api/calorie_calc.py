from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL

calorie_calc = Blueprint("calorie_calc", __name__)

from manage import mysql

@calorie_calc.route('', methods=['GET'])
def calc_cal():
    try:
        return Response(json.dumps({"Daily calorie to consume": 2000, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to calculate calories."}