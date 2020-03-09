from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL

user = Blueprint("user", __name__)

from manage import mysql as mysql
from manage import bcrypt as bcrypt

@user.route('/all', methods=['GET'])
def get_all_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BiteBody.Users;")
        all_users = []
        rows = cur.fetchall()
        for row in rows:
            temp_user = {}
            temp_user['id'] = row[0]
            temp_user['first_name'] = row[1]
            temp_user['last_name'] = row[2]
            temp_user['email'] = row[3]
            all_users.append(temp_user)
        return Response(json.dumps({"users": all_users, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrive all users."}

@user.route('/<int:userID>', methods=['GET'])
def find_user(userID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BiteBody.Users WHERE id = "+str(userID)+";")
        row = cur.fetchone()
        user = {
            'first_name':row[1],
            'last_name':row[2],
            'email' : row[3],
            'id' : row[0]
        }
        return Response(json.dumps({"user": user, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrieve this user."}
        
@user.route('/<int:userID>', methods=['DELETE'])
def delete_user(userID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM Bitebody.Users Where id = " +str(userID) +  ";")
        row = cur.fetchone()
        foundID = row[0]
        if foundID == None:
            return {"NOT FOUND":"User want to delete doesn't exist"}
        else:
            cur.execute("DELETE FROM BiteBody.Users WHERE id = " + str(userID) + ";")
            mysql.connection.commit()
            deleted = {
                'id' : userID 
            }
            return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to delete this user."}

@user.route('/<int:userID>', methods = ['PUT'])
def update_user_info(userID):
    try:
        cur = mysql.connection.cursor()
        first_name = request.get_json()['first_name']
        last_name = request.get_json()['last_name']
        email = request.get_json()['email']
        password = request.get_json()['password']
        cur.execute("UPDATE BiteBody.Users SET first_name = '"+str(first_name) + "',last_name = '" + str(last_name)+ "',email = '"+ str(email)+"',password = '"+ str(password) + 
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
        return {"Error": "Unable to update this user."}

@user.route('', methods=['POST'])
def create_user():
    try:
        cur = mysql.connection.cursor()
        first_name = request.get_json()['first_name']
        last_name = request.get_json()['last_name']
        email = request.get_json()['email']

        cur.execute("SELECT email FROM BiteBody.Users WHERE email = '" + email +"';")
        emailFound = cur.fetchone()
        print("Email Found value: ", emailFound)
        if(emailFound):
            return {"Error": "Can't add already existing email"}
        else:
            password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
            cur.execute("INSERT INTO BiteBody.Users (first_name, last_name, email, password) VALUES ('" 
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
    except Exception as e:
        print(e)
        return {"Error": "Unable to create this user.", "code": 400, "ErrorMessage": str(e)}

@user.route('/login', methods=['POST'])
def login():
    try:
        cur = mysql.connection.cursor()
        email = request.get_json()['email']
        password = request.get_json()['password']
        cur.execute("SELECT * FROM BiteBody.Users where email = '" + str(email) + "'")
        rv = cur.fetchone()
        result = {}
        print(rv[4])
        print(password)

        if bcrypt.check_password_hash(rv[4], password):
            print("Passwords Match!")
        else:
            raise Exception('Passwords do not match')
        
        return {"Allow": "yes"}

    except Exception as e:
        print (e)
        return {
            "Error": "Incorrect email or password.",
            "Allow": "no"
        }