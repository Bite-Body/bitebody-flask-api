from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL

collab = Blueprint("collab", __name__)

from manage import mysql

@collab.route('/all', methods=['GET'])
def get_all_collabs():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BiteBody.Collaborators;")
        all_collabs = []
        rows = cur.fetchall()
        for row in rows:
            temp_collab = {}
            temp_collab['id'] = row[0]
            temp_collab['youtube_link'] = row[1]
            all_collabs.append(temp_collab)
        return Response(json.dumps({"collabs": all_collabs, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrive all collaborators."}

@collab.route('/<int:collabID>', methods=['GET'])
def find_collaborator(collabID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BiteBody.Collaborators WHERE id = "+str(collabID)+";")
        row = cur.fetchone()
        collab = {
            'youtube_link':row[1],
            'id' : row[0]
        }
        return Response(json.dumps({"collaborator": collab, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrieve this collaborator."}
   
@collab.route('/<int:collabID>', methods=['DELETE'])
def delete_collab(collabID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM BiteBody.Collaborators WHERE id = " + str(collabID) + ";")
        mysql.connection.commit()
        deleted = {
            'id' : collabID
        }
        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to delete this collaborator."}

@collab.route('/<int:collabID>', methods = ['PUT'])
def update_collab_info(collabID):
    try:
        cur = mysql.connection.cursor()
        youtube_link = request.get_json()['youtube_link']
        cur.execute("UPDATE BiteBody.Collaborators SET youtube_link = '"+str(youtube_link) + 
        "'WHERE id = "+ str(collabID)+";")
        mysql.connection.commit()
        updated = {
            'youtube_link':youtube_link
        }
        return Response(json.dumps({"updated": updated, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to update this collaborator."}

@collab.route('', methods=['POST'])
def create_collab():
    try:
        cur = mysql.connection.cursor()
        id = request.get_json()['id']
        youtube_link = request.get_json()['youtube_link']
        cur.execute("INSERT INTO BiteBody.Collaborators (id, youtube_link) VALUES ('" 
            + id + "', '" 
            + youtube_link + "');")
        mysql.connection.commit()
        posted = {
            'youtube link' : youtube_link,
            'id' : id
        }
        return Response(json.dumps({"posted": posted, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to create this collaborator."}
