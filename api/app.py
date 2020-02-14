from flask import Flask, Response, jsonify, json, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'ODK1LCc5DZ'
app.config['MYSQL_PASSWORD'] = 'pN8S7PFHib'
app.config['MYSQL_DB'] = 'ODK1LCc5DZ'

mysql = MySQL(app)

@app.route('/')
def hello_world():
    return 'Hello, welcome to api.bitebody.xyz! \nThe following below are our endpoints...'

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

        ##COLLABORATOR table endpoints

        
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
        #temp_user['last_name'] = row[2]
       # temp_user['email'] = row[3]
        # temp_user['password'] = row[4] don't send this lol
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
        #first_name = request.get_json()['first_name']
        #last_name = request.get_json()['last_name']
        #email = request.get_json()['email']
        #password = request.get_json()['password']
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
