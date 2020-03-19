from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL

workout = Blueprint("workout", __name__)

from manage import mysql

@workout.route('/all', methods=['GET'])
def get_all_workouts():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * From BiteBody.Workouts;")
        all_workouts = []
        rows = cur.fetchall()
        for row in rows:
            temp_workout = {}
            temp_workout['id'] = row[0]
            temp_workout['workout_name'] = row[1] 
            temp_workout['workout_description'] = row[2]
            temp_workout['workout_image_path'] = row[3]
            temp_workout['genre'] = row[4]
            temp_workout['body_part'] = row[5]
            temp_workout['duration'] = row[6]
            temp_workout['equipment'] = row[7]
            all_workouts.append(temp_workout)
        return Response(json.dumps({"workouts": all_workouts, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrive all workouts.", "error message": str(e)}

@workout.route('/<int:wkoutID>', methods=['GET'])
def find_workout(wkoutID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BiteBody.Workouts WHERE id = "+str(wkoutID)+";")
        row = cur.fetchone()
        workout = {
            'id' : row[0],
            'workout_name':row[1],
            'workout_description':row[2],
            'workout_image_path' : row[3],
            'genre': row[4],
            'body_part': row[5],
            'duration': row[6],
            'equipment': row[7]
        }
        return Response(json.dumps({"workout": workout, "code": 200}), mimetype='application/json')
    except Exception as e:

        return {"Error": "Unable to retrieve this workout.", "error message": str(e)}

@workout.route('/<int:wkoutID>', methods=['DELETE'])
def delete_workout(wkoutID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM BiteBody.Workouts WHERE id = " + str(wkoutID) + ";")
        mysql.connection.commit()
        deleted = {
            'id' : wkoutID
        }
        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to delete this workout.", "error message": str(e)}

@workout.route('/<int:wkoutID>', methods = ['PUT'])
def update_workout_info(wkoutID):
    try:
        cur = mysql.connection.cursor()
        workout_name = request.get_json()['workout_name']
        workout_description = request.get_json()['workout_description']
        workout_image_path = request.get_json()['workout_image_path']
        genre = request.get_json()['genre']
        body_part = request.get_json()['body_part']
        duration = request.get_json()['duration']
        equipment = request.get_json()['equipment']
            
        cur.execute("UPDATE BiteBody.Workouts SET workout_name = '"+str(workout_name) + "',workout_description = '" + str(workout_description)+ "',workout_image_path = '"+ 
        str(workout_image_path)+"',genre = '"+ str(genre) + "',body_part = '" + str(body_part)+"',duration = '" + str(duration)+"',equipment = '" + str(equipment)+
        "'WHERE id = "+ str(wkoutID)+";")
        mysql.connection.commit()
        workout = { 
            'id': wkoutID,
            'workout_name': workout_name,
            'workout_description': workout_description,
            'workout_image_path' : workout_image_path,
            'genre': genre,
            'body_part': body_part,
            'duration': duration,
            'equipment': equipment
        }
        return Response(json.dumps({"updated": workout, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to update this workout.", "error message": str(e)}

@workout.route('', methods=['POST'])
def insert_workout():
    try:
        cur = mysql.connection.cursor()
        id = request.get_json()['id']
        workout_name = request.get_json()['workout_name']
        workout_description = request.get_json()['workout_description']
        workout_image_path = request.get_json()['workout_image_path']
        genre = request.get_json()['genre']
        body_part = request.get_json()['body_part']
        duration = request.get_json()['duration']
        equipment = request.get_json()['equipment']
        cur.execute("INSERT INTO BiteBody.Workouts (id, workout_name, workout_description, workout_image_path, genre, body_part, duration, equipment) VALUES ('" 
            + id + "', '" 
            + workout_name + "', '" 
            + workout_description + "', '" 
            + workout_image_path + "', '"
            + genre + "', '"  
            + body_part + "', '" 
            + duration + "', '" 
            + equipment + "');")
        mysql.connection.commit()
        workout = { 
            'id': id,
            'workout_name': workout_name,
            'workout_description': workout_description,
            'workout_image_path' : workout_image_path,
            'genre': genre,
            'body_part': body_part,
            'duration': duration,
            'equipment': equipment
        }
        return Response(json.dumps({"workout added": workout, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to create this workout.", "error message": str(e)}
