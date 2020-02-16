from flask import Flask, Response, jsonify, json, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'ODK1LCc5DZ'
app.config['MYSQL_PASSWORD'] = 'pN8S7PFHib'
app.config['MYSQL_DB'] = 'ODK1LCc5DZ'

mysql = MySQL(app)

CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, welcome to api.bitebody.xyz! \nThe following below are our endpoints...'
#-----------------------USER-METHODS-START----------------------#
@app.route('/users/all', methods=['GET'])
def get_all_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ODK1LCc5DZ.Users;")

    all_users = []

    rows = cur.fetchall()

    for row in rows:
        temp_user = {}
        temp_user['id'] = row[0]
        temp_user['first_name'] = row[1]
        temp_user['last_name'] = row[2]
        temp_user['email'] = row[3]
        # temp_user['password'] = row[4] don't send this lol
        all_users.append(temp_user)

    # https://stackoverflow.com/questions/29020839/mysql-fetchall-how-to-get-data-inside-a-dict-rather-than-inside-a-tuple
    # These two lines zips the resulting values with cursor.description
    # columns = [col[0] for col in cur.description]
    # rows = [dict(zip(columns, row)) for row in cur.fetchall()]

    return Response(json.dumps({"users": all_users, "code": 200}), mimetype='application/json')

@app.route('/users/<int:userID>', methods=['DELETE'])
def delete_user(userID):
    try:
        cur = mysql.connection.cursor()


        cur.execute("DELETE FROM ODK1LCc5DZ.Users WHERE id = " + str(userID) + ";")
        mysql.connection.commit()

        deleted = {
            'id' : userID
        }

        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}

@app.route('/users', methods=['POST'])
def create_user():
    cur = mysql.connection.cursor()

    print(request.get_json())

    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = request.get_json()['password']

    cur.execute("INSERT INTO ODK1LCc5DZ.Users (first_name, last_name, email, password) VALUES ('" 
        + first_name + "', '" 
        + last_name + "', '" 
        + email + "', '" 
        + password + "');")

    mysql.connection.commit()

    posted = {
		'first_name' : first_name,
		'last_name' : last_name,
		'email' : email,
		'password' : password
	}
    
    return Response(json.dumps({"posted": posted, "code": 201}), mimetype='application/json')

@app.route('/users/<int:userID>', methods = ['PUT'])
def update_user_info(userID):
    try:
        cur = mysql.connection.cursor()
        first_name = request.get_json()['first_name']
        last_name = request.get_json()['last_name']
        email = request.get_json()['email']
        password = request.get_json()['password']
            

        cur.execute("UPDATE ODK1LCc5DZ.Users SET first_name = '"+str(first_name) + "',last_name = '" + str(last_name)+ "',email = '"+ str(email)+"',password = '"+ str(password) + 
        "'WHERE id = "+ str(userID)+";")
        mysql.connection.commit()
        updated = {
                'first_name':first_name,
                'last_name':last_name,
                'email' : email,
                'password' : password
            }
            

        return Response(json.dumps({"updated": updated, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}

@app.route('/users/<int:userID>', methods=['GET'])
def find_user(userID):
    try:
        cur = mysql.connection.cursor()
        

        cur.execute("SELECT * FROM ODK1LCc5DZ.Users WHERE id = "+str(userID)+";")
        row = cur.fetchone()
        
        user = {
                'first_name':row[1],
                'last_name':row[2],
                'email' : row[3],
                'id' : row[0]
            }

        

        return Response(json.dumps({"user": user, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}

@app.route('/users/login', methods=['POST'])
def login():
    try:
        cur = mysql.connection.cursor()
        email = request.get_json()['email']
        password = request.get_json()['password']
        
        
        cur.execute("SELECT * FROM ODK1LCc5DZ.Users where email = '" + str(email) + "'")
        rv = cur.fetchone()
        
        if (rv[4] == password):
            
            print("Password Match")
        else:
            print("Password not matching")
        
        return {"error": "nah"}
    except Exception as e:
        print(e)
        return {"error": "yep"}

#-----------------------USER-METHODS-END----------------------#

        ##COLLABORATOR table endpoints

#---------------------Collaborator-Endpoints-Start---------------------#       
@app.route('/collabs/all', methods=['GET'])
def get_all_collabs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ODK1LCc5DZ.Collaborator;")

    all_collabs = []

    rows = cur.fetchall()

    for row in rows:
        temp_collab = {}
        temp_collab['id'] = row[0]
        temp_collab['youtube_link'] = row[1]
        all_collabs.append(temp_collab)

    # https://stackoverflow.com/questions/29020839/mysql-fetchall-how-to-get-data-inside-a-dict-rather-than-inside-a-tuple
    # These two lines zips the resulting values with cursor.description
    # columns = [col[0] for col in cur.description]
    # rows = [dict(zip(columns, row)) for row in cur.fetchall()]

    return Response(json.dumps({"users": all_collabs, "code": 404}), mimetype='application/json')



@app.route('/collabs/<int:collabID>', methods=['GET'])
def find_collaborator(collabID):
    try:
        cur = mysql.connection.cursor()
        

        cur.execute("SELECT * FROM ODK1LCc5DZ.Collaborator WHERE id = "+str(collabID)+";")
        row = cur.fetchone()
        
        collab = {
                'youtube_link':row[1],
                'id' : row[0]
            }

        

        return Response(json.dumps({"collaborator": collab, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}



@app.route('/collabs', methods=['POST'])
def create_collab():
    cur = mysql.connection.cursor()

    print(request.get_json())

    id = request.get_json()['id']
    youtube_link = request.get_json()['youtube_link']

    cur.execute("INSERT INTO ODK1LCc5DZ.Collaborator (id, youtube_link) VALUES ('" 
        + id + "', '" 
        + youtube_link + "');")

    mysql.connection.commit()

    posted = {
		'youtube link' : youtube_link,
		'id' : id
	}
    
    return Response(json.dumps({"posted": posted, "code": 201}), mimetype='application/json')


@app.route('/collabs/<int:collabID>', methods = ['PUT'])
def update_collab_info(collabID):
    try:
        cur = mysql.connection.cursor()

        youtube_link = request.get_json()['youtube_link']
            

        cur.execute("UPDATE ODK1LCc5DZ.Collaborator SET youtube_link = '"+str(youtube_link) + 
        "'WHERE id = "+ str(collabID)+";")
        mysql.connection.commit()
        updated = {
                'youtube_link':youtube_link
            }
            

        return Response(json.dumps({"updated": updated, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}


@app.route('/collabs/<int:collabID>', methods=['DELETE'])
def delete_collab(collabID):
    try:
        cur = mysql.connection.cursor()


        cur.execute("DELETE FROM ODK1LCc5DZ.Collaborator WHERE id = " + str(collabID) + ";")
        mysql.connection.commit()

        deleted = {
            'id' : collabID
        }

        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}

        ##COLLABORATOR table endpoints
        #David's Contributions WOAH
#---------------------Collaborator-Endpoints-End---------------------# 


#---------------------Workout-Endpoints-Start---------------------# 
#GET ALL WORKOUTS
@app.route('/workouts/all', methods = ['GET'])
def get_all_workouts():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * From ODK1LCc5DZ.Workouts;")

        all_workouts = []

        rows = cur.fetchall()

        for row in rows:
            temp_workout = {}
            temp_workout['id'] = row[0]
            temp_workout['wkout_name'] = row[1] 
            temp_workout['wkout_description'] = row[2]
            temp_workout['wkout_image_path'] = row[3]
            temp_workout['genre'] = row[4]
            temp_workout['body_part'] = row[5]
            temp_workout['duration'] = row[6]
            temp_workout['equipment'] = row[7]
            all_workouts.append(temp_workout)
            

        
            

        return Response(json.dumps({"workouts": all_workouts, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yes"}

#GET SPECIFIC WORKOUTS
@app.route('/workouts/<int:wkoutID>', methods=['GET'])
def find_workout(wkoutID):
    try:
        cur = mysql.connection.cursor()
        

        cur.execute("SELECT * FROM ODK1LCc5DZ.Workouts WHERE wkout_ID = "+str(wkoutID)+";")
        row = cur.fetchone()
        
        workout = {
                'id' : row[0],
                'Workout_name':row[1],
                'workout_description':row[2],
                'workout_image_path' : row[3],
                'Genre': row[4],
                'body_part': row[5],
                'duration': row[6],
                'equipment': row[7]
                
            }

        

        return Response(json.dumps({"workout": workout, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}
#ADD A WORKOUT
@app.route('/workouts', methods=['POST'])
def insert_workout():
    cur = mysql.connection.cursor()

    print(request.get_json())

    wkout_ID = request.get_json()['wkout_ID']
    wkout_name = request.get_json()['wkout_name']
    wkout_description = request.get_json()['wkout_description']
    wkout_image_path = request.get_json()['wkout_image_path']
    genre = request.get_json()['genre']
    body_part = request.get_json()['body_part']
    duration = request.get_json()['duration']
    equipment = request.get_json()['equipment']

    cur.execute("INSERT INTO ODK1LCc5DZ.Workouts (wkout_ID, wkout_name, wkout_description, wkout_image_path, genre, body_part, duration, equipment) VALUES ('" 
        + wkout_ID + "', '" 
        + wkout_name + "', '" 
        + wkout_description + "', '" 
        + wkout_image_path + "', '"
        + genre + "', '"  
        + body_part + "', '" 
        + duration + "', '" 
        + equipment + "');")

    mysql.connection.commit()

    workout = { 
                'wkout_ID': wkout_ID,
                'wkout_name': wkout_name,
                'wkout_description': wkout_description,
                'wkout_image_path' : wkout_image_path,
                'Genre': genre,
                'body_part': body_part,
                'duration': duration,
                'equipment': equipment
                
            }
    
    return Response(json.dumps({"workout added": workout, "code": 201}), mimetype='application/json')

#UPDATE A WORKOUT
@app.route('/workouts/<int:wkoutID>', methods = ['PUT'])
def update_workout_info(wkoutID):
    try:
        cur = mysql.connection.cursor()
        wkout_name = request.get_json()['wkout_name']
        wkout_description = request.get_json()['wkout_description']
        wkout_image_path = request.get_json()['wkout_image_path']
        genre = request.get_json()['genre']
        body_part = request.get_json()['body_part']
        duration = request.get_json()['duration']
        equipment = request.get_json()['equipment']
            

        cur.execute("UPDATE ODK1LCc5DZ.Workouts SET wkout_name = '"+str(wkout_name) + "',wkout_description = '" + str(wkout_description)+ "',wkout_image_path = '"+ 
        str(wkout_image_path)+"',genre = '"+ str(genre) + "',body_part = '" + str(body_part)+"',duration = '" + str(duration)+"',equipment = '" + str(equipment)+
        "'WHERE wkout_ID = "+ str(wkoutID)+";")
        mysql.connection.commit()
        workout = { 
                'wkout_ID': wkoutID,
                'wkout_name': wkout_name,
                'wkout_description': wkout_description,
                'wkout_image_path' : wkout_image_path,
                'Genre': genre,
                'body_part': body_part,
                'duration': duration,
                'equipment': equipment
                
            }
            

        return Response(json.dumps({"updated": workout, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}

#DELETE WORKOUT
@app.route('/workouts/<int:wkoutID>', methods=['DELETE'])
def delete_workout(wkoutID):
    try:
        cur = mysql.connection.cursor()


        cur.execute("DELETE FROM ODK1LCc5DZ.Workouts WHERE wkout_ID = " + str(wkoutID) + ";")
        mysql.connection.commit()

        deleted = {
            'id' : wkoutID
        }

        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}
#---------------------WORKOUTS-ENDPOINTS-END---------------------# 