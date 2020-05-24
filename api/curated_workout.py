from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL
from logger import post_log

curated_workout = Blueprint("curated_workout", __name__)

from manage import mysql

@curated_workout.route('/all', methods=['GET'])
def get_all_workouts():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * From heroku_012605fb848c7a7.curated_workout;")
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

        post_log('GET /curated_workout/all')
        return Response(json.dumps({"curated_workouts": all_workouts, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrive all curated workouts.", "ErrorMessage": str(e)}

@curated_workout.route('/<string:workout_type>', methods=['GET'])
def find_workout_by_type(workout_type):
    try:
        print(workout_type)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM heroku_012605fb848c7a7.curated_workout WHERE workout_type = \"" + str(workout_type) + "\";")
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
            all_workouts.append(temp_workout)

        post_log('GET /curated_workout/<string:workout_type>')
        return Response(json.dumps({"curated_workout": all_workouts, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrieve this workout.", "ErrorMessage": str(e)}

@curated_workout.route('/<int:wkoutID>', methods=['GET'])
def find_workout(wkoutID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM heroku_012605fb848c7a7.curated_workout WHERE id = "+str(wkoutID)+";")
        row = cur.fetchone()
        workout = {
            'id' : row[0],
            'name':row[1],
            'goal':row[2],
            'workout_type' : row[3],
            'level': row[4],
            'days_per_week': row[5],
            'time_per_week': row[6],
            'targeted_gender': row[7],
            'workout_pdf': row[8],
        }

        post_log('GET /curated_workout/<int:wkoutID>')
        return Response(json.dumps({"curated_workout": workout, "code": 200}), mimetype='application/json')
    except Exception as e:

        return {"Error": "Unable to retrieve this workout.", "ErrorMessage": str(e)}

@curated_workout.route('/<int:wkoutID>', methods=['DELETE'])
def delete_workout(wkoutID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM heroku_012605fb848c7a7.curated_workout WHERE id = " + str(wkoutID) + ";")
        mysql.connection.commit()
        deleted = {
            'id' : wkoutID
        }

        post_log('DELETE /curated_workout/<int:wkoutID>')
        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to delete this workout.", "ErrorMessage": str(e)}

#FINISH THIS!#
@curated_workout.route('/<int:wkoutID>', methods = ['PUT'])
def update_workout_info(wkoutID):
    try:
        cur = mysql.connection.cursor()
        name = request.get_json()['name']
        goal = request.get_json()['goal']
        workout_type = request.get_json()['workout_type']
        level = request.get_json()['level']
        days_per_week = request.get_json()['days_per_week']
        time_per_workout = request.get_json()['time_per_workout']
        targeted_gender = request.get_json()['targeted_gender']
        workout_pdf = request.get_json()['workout_pdf']
        #STOPPED HERE

        cur.execute("UPDATE heroku_012605fb848c7a7.curated_workout SET name = '"+str(name) + "',goal = '" + str(goal)+ "',workout_type = '"+ 
        str(workout_type)+"',level = '"+ str(level) + "',days_per_week = '" + str(days_per_week)+"',time_per_workout = '" + str(time_per_workout)+"',targeted_gender = '" + str(targeted_gender)+ "',workout_pdf = '" + str(workout_pdf)+ 
        "'WHERE id = "+ str(wkoutID)+";")
        mysql.connection.commit()
        workout = { 
            'id' : wkoutID,
            'name': name,
            'goal': goal,
            'workout_type' : workout_type,
            'level': level,
            'days_per_week': days_per_week,
            'time_per_week': time_per_week,
            'targeted_gender': targeted_gender,
            'workout_pdf': workout_pdf,
        }

        post_log('PUT /curated_workout/<int:wkoutID>')
        return Response(json.dumps({"updated": workout, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to update this workout.", "ErrorMessage": str(e)}


@curated_workout.route('', methods=['POST'])
def insert_workout():
    try:
        cur = mysql.connection.cursor()
        id = request.get_json()['id']
        name = request.get_json()['name']
        goal = request.get_json()['goal']
        workout_type = request.get_json()['workout_type']
        level = request.get_json()['level']
        days_per_week = request.get_json()['days_per_week']
        time_per_workout = request.get_json()['time_per_workout']
        targeted_gender = request.get_json()['targeted_gender']
        workout_pdf = request.get_json()['workout_pdf']
        image = request.get_json()['image']
        
        cur.execute("INSERT INTO heroku_012605fb848c7a7.curated_workout (id, name, goal, workout_type, level, days_per_week, time_per_workout, targeted_gender, workout_pdf, image) VALUES ('" 
            + id + "', '" 
            + name + "', '" 
            + goal + "', '" 
            + workout_type + "', '"
            + level + "', '"  
            + days_per_week + "', '"
            + time_per_workout + "', '"
            + targeted_gender + "', '"
            + workout_pdf + "', '" 
            + image + "');")
        mysql.connection.commit()
        workout = { 
            'id': id,
            'name': name,
            'goal': goal,
            'workout_type' : workout_type,
            'level': level,
            'days_per_week': days_per_week,
            'time_per_workout': time_per_workout,
            'targeted_gender': targeted_gender,
            'workout_pdf': workout_pdf,
            'image': image
            
        }

        post_log('POST /curated_workouts')
        return Response(json.dumps({"curated workout added": workout, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to create this workout.", "ErrorMessage":str(e)}