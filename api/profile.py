from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL
from logger import post_log

profile = Blueprint("profile", __name__)

from manage import mysql

@profile.route('/<int:profileID>', methods=['GET'])
def find_profile_data(profileID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM heroku_012605fb848c7a7.profile_data WHERE id = "+str(profileID)+";")
        row = cur.fetchone()
        data = {
            'id' : row[0],
            'nickname': row[1],
            'title': row[2],
            'age' : row[3],
            'bio' : row[4],
            'gender' : row[5]
        }

        post_log('GET /profile/' + str(profileID))
        return Response(json.dumps({"profile_data": data, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrieve this profile data."}

@profile.route('', methods=['POST'])
def update_profile():
    try:
        cur = mysql.connection.cursor()
        id = str(request.get_json()['id'])
        age = request.get_json()['age']
        bio = request.get_json()['bio']
        gender = request.get_json()['gender']
        nickname = request.get_json()['nickname']
        title = request.get_json()['title']

        cur.execute("INSERT INTO heroku_012605fb848c7a7.profile_data (id, nickname, title, age, bio, gender) VALUES ('" 
            + id + "', '" 
            + nickname + "', '"
            + title + "', '" 
            + age + "', '" 
            + bio + "', '" 
            + gender + "');")

        mysql.connection.commit()

        post_log('POST /profile')
        return Response(json.dumps({"profile_updated": "successful", "code": 201}), mimetype='application/json')
    except Exception as e:
        try:
        # we finna update if post fails
            cur.execute("UPDATE heroku_012605fb848c7a7.profile_data SET id = '"+ id + 
            "',nickname = '" + nickname + 
            "',title = '" + title +
            "',age = '" + age +
            "',bio = '" + bio +
            "',gender = '" + gender +
            "'WHERE id = "+ id +";")
            mysql.connection.commit()
            return Response(json.dumps({"profile_updated": "successful but with UPDATE", "code": 201}), mimetype='application/json')
        except Exception as e:
            return {"Error": f"sir we failed not once, but twice. Twas the issue: {e}"}

        return {"Error": f"Unable to create this profile data. {e}"}