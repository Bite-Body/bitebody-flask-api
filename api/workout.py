from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL
from logger import post_log

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
            temp_workout['main_muscle_group'] = row[2]
            temp_workout['detailed_muscle_group'] = row[3]
            temp_workout['other_muscle_groups'] = row[4]
            temp_workout['type'] = row[5]
            temp_workout['mechanics'] = row[6]
            temp_workout['equipment'] = row[7]
            temp_workout['difficulty'] = row[8]
            temp_workout['exercise_steps'] = row[9]
            temp_workout['image_path'] = row[10]
            all_workouts.append(temp_workout)

        post_log('GET /workouts/all')
        return Response(json.dumps({"workouts": all_workouts, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrive all workouts.", "ErrorMessage": str(e)}

@workout.route('/<string:workout_type>', methods=['GET'])
def find_workout_by_type(workout_type):
    try:
        print(workout_type)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BiteBody.Workouts WHERE main_muscle_group = \"" + str(workout_type) + "\";")
        all_workouts = []
        rows = cur.fetchall()
        for row in rows:
            temp_workout = {}
            temp_workout['id'] = row[0]
            temp_workout['workout_name'] = row[1] 
            temp_workout['main_muscle_group'] = row[2]
            temp_workout['detailed_muscle_group'] = row[3]
            temp_workout['other_muscle_groups'] = row[4]
            temp_workout['type'] = row[5]
            temp_workout['mechanics'] = row[6]
            temp_workout['equipment'] = row[7]
            temp_workout['difficulty'] = row[8]
            temp_workout['exercise_steps'] = row[9]
            temp_workout['image_path'] = row[10]
            all_workouts.append(temp_workout)

        post_log('GET /workouts/<string:workout_type>')
        return Response(json.dumps({"workouts": all_workouts, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrieve this workout.", "ErrorMessage": str(e)}

@workout.route('/<int:wkoutID>', methods=['GET'])
def find_workout(wkoutID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BiteBody.Workouts WHERE id = "+str(wkoutID)+";")
        row = cur.fetchone()
        workout = {
            'id' : row[0],
            'workout_name':row[1],
            'main_muscle_group':row[2],
            'detailed_muscle_group' : row[3],
            'other_muscle_group': row[4],
            'type': row[5],
            'mechanics': row[6],
            'equipment': row[7],
            'difficulty': row[8],
            'exercise_steps': row[9],
            'image_path': row[10]
        }

        post_log('GET /workouts/<int:wkoutID>')
        return Response(json.dumps({"workout": workout, "code": 200}), mimetype='application/json')
    except Exception as e:

        return {"Error": "Unable to retrieve this workout.", "ErrorMessage": str(e)}

@workout.route('/<int:wkoutID>', methods=['DELETE'])
def delete_workout(wkoutID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM BiteBody.Workouts WHERE id = " + str(wkoutID) + ";")
        mysql.connection.commit()
        deleted = {
            'id' : wkoutID
        }

        post_log('DELETE /workouts/<int:wkoutID>')
        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to delete this workout.", "ErrorMessage": str(e)}

@workout.route('/<int:wkoutID>', methods = ['PUT'])
def update_workout_info(wkoutID):
    try:
        cur = mysql.connection.cursor()
        workout_name = request.get_json()['workout_name']
        main_muscle_group = request.get_json()['main_muscle_group']
        detailed_muscle_group = request.get_json()['detailed_muscle_group']
        other_muscle_groups = request.get_json()['other_muscle_groups']
        type_ = request.get_json()['type']
        mechanics = request.get_json()['mechanics']
        equipment = request.get_json()['equipment']
        difficulty = request.get_json()['difficulty']
        excercise_steps = request.get_json()['excercise_steps']
        image_path = request.get_json()['image_path']
            
        cur.execute("UPDATE BiteBody.Workouts SET workout_name = '"+str(workout_name) + "',main_muscle_group = '" + str(main_muscle_group)+ "',detailed_muscle_group = '"+ 
        str(detailed_muscle_group)+"',other_muscle_groups = '"+ str(other_muscle_groups) + "',type = '" + str(type_)+"',mechanics = '" + str(mechanics)+"',equipment = '" + str(equipment)+ "',difficulty = '" + str(difficulty)+ "',excercise_steps = '" + str(excercise_steps)+ "',image_path = '" + str(image_path)+
        "'WHERE id = "+ str(wkoutID)+";")
        mysql.connection.commit()
        workout = { 
            'id' : wkoutID,
            'workout_name': workout_name,
            'main_muscle_group': main_muscle_group,
            'detailed_muscle_group' : detailed_muscle_group,
            'other_muscle_groups': other_muscle_groups,
            'type': type_,
            'mechanics': mechanics,
            'equipment': equipment,
            'difficulty': difficulty,
            'excercise_steps': excercise_steps,
            'image_path': image_path
        }

        post_log('PUT /workouts/<int:wkoutID>')
        return Response(json.dumps({"updated": workout, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to update this workout.", "ErrorMessage": str(e)}

@workout.route('', methods=['POST'])
def insert_workout():
    try:
        cur = mysql.connection.cursor()
        id = request.get_json()['id']
        workout_name = request.get_json()['workout_name']
        main_muscle_group = request.get_json()['main_muscle_group']
        detailed_muscle_group = request.get_json()['detailed_muscle_group']
        other_muscle_groups = request.get_json()['other_muscle_groups']
        type_ = request.get_json()['type']
        mechanics = request.get_json()['mechanics']
        equipment = request.get_json()['equipment']
        difficulty = request.get_json()['difficulty']
        excercise_steps = request.get_json()['excercise_steps']
        image_path = request.get_json()['image_path']
        cur.execute("INSERT INTO BiteBody.Workouts (id, workout_name, main_muscle_group, detailed_muscle_group, other_muscle_groups, type, mechanics, equipment, difficulty, excercise_steps,image_path) VALUES ('" 
            + id + "', '" 
            + workout_name + "', '" 
            + main_muscle_group + "', '" 
            + detailed_muscle_group + "', '"
            + other_muscle_groups + "', '"  
            + type_ + "', '"
            + mechanics + "', '"
            + equipment + "', '"
            + difficulty + "', '" 
            + excercise_steps + "', '" 
            + image_path + "');")
        mysql.connection.commit()
        workout = { 
            'id': id,
            'workout_name': workout_name,
            'main_muscle_group': main_muscle_group,
            'detailed_muscle_group' : detailed_muscle_group,
            'other_muscle_groups': other_muscle_groups,
            'type': type_,
            'mechanics': mechanics,
            'equipment': equipment,
            'difficulty': difficulty,
            'excercise_steps': excercise_steps,
            'image_path': image_path
        }

        post_log('POST /workouts')
        return Response(json.dumps({"workout added": workout, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to create this workout.", "ErrorMessage":str(e)}
