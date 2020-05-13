from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL
from logger import post_log

curated_workout = Blueprint("Weight_Loss", __name__)

from manage import mysql

@curated_workout.route('/all', methods=['GET'])
def get_all_workouts():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * From BiteBody.Weight_Loss;")
        all_workouts = []
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
            all_workouts.append(temp_workout)

        post_log('GET /Weight_Loss/all')
        return Response(json.dumps({"Weight_Loss": all_workouts, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrive all weight loss strats.", "ErrorMessage": str(e)}