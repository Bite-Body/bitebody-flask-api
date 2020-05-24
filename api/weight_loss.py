from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL
from logger import post_log

weight_loss = Blueprint("weight_loss", __name__)

from manage import mysql

@weight_loss.route('/all', methods=['GET'])
def get_all_weight_loss():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * From heroku_012605fb848c7a7.weight_loss;")
        all_weight_loss = []
        rows = cur.fetchall()
        for row in rows:
            temp_workout = {}
            temp_workout['id'] = row[0]
            temp_workout['name'] = row[1] 
            temp_workout['goal'] = row[2]
            temp_workout['workout_type'] = row[3]
            temp_workout['level'] = row[4]
            temp_workout['days_per_week'] = row[5]
            temp_workout['time_per_workout'] = row[6]
            temp_workout['targeted_gender'] = row[7]
            temp_workout['workout_pdf'] = row[8]
            temp_workout['image'] = row[9]
            all_weight_loss.append(temp_workout)

        post_log('GET /weight_loss/all')
        return Response(json.dumps({"Weight_Loss": all_weight_loss, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrive all weight loss strats.", "ErrorMessage": str(e)}