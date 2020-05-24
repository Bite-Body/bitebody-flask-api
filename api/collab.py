from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL
from logger import post_log

collab = Blueprint("collab", __name__)

from manage import mysql

@collab.route('/all', methods=['GET'])
def get_all_collabs():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM heroku_012605fb848c7a7.collaborators;")
        all_collabs = []
        rows = cur.fetchall()
        for row in rows:
            temp_collab = {}
            temp_collab['id'] = row[0]
            temp_collab['youtube_link'] = row[1]
            all_collabs.append(temp_collab)

        post_log('GET /collabs/all')
        return Response(json.dumps({"collabs": all_collabs, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrive all collaborators.","error message": str(e)}

@collab.route('/<int:collabID>', methods=['GET'])
def find_collaborator(collabID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM heroku_012605fb848c7a7.collaborators WHERE id = "+str(collabID)+";")
        row = cur.fetchone()
        collab = {
            'youtube_link':row[1],
            'id' : row[0]
        }

        post_log('GET /meals/<int:collabID>')
        return Response(json.dumps({"collaborator": collab, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrieve this collaborator.","error message": str(e)}
   
@collab.route('/<int:collabID>', methods=['DELETE'])
def delete_collab(collabID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM heroku_012605fb848c7a7.collaborators WHERE id = " + str(collabID) + ";")
        mysql.connection.commit()
        deleted = {
            'id' : collabID
        }

        post_log('DELETE /meals/<int:collabID>')
        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to delete this collaborator.","error message": str(e)}

@collab.route('/<int:collabID>', methods = ['PUT'])
def update_collab_info(collabID):
    try:
        cur = mysql.connection.cursor()
        youtube_link = request.get_json()['youtube_link']
        cur.execute("UPDATE heroku_012605fb848c7a7.collaborators SET youtube_link = '"+str(youtube_link) + 
        "'WHERE id = "+ str(collabID)+";")
        mysql.connection.commit()
        updated = {
            'youtube_link':youtube_link
        }

        post_log('PUT /meals/<int:collabID>')
        return Response(json.dumps({"updated": updated, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to update this collaborator." ,"error message": str(e)}

@collab.route('', methods=['POST'])
def create_collab():
    try:
        cur = mysql.connection.cursor()
        id = request.get_json()['id']
        youtube_link = request.get_json()['youtube_link']

        cur.execute("SELECT id FROM BiteBody.Users Where id = " +str(id) +  ";")
        row = cur.fetchone()
        foundID = row[0]
        #print("row: ", row)
        #print("foundID: ", foundID)
        
        #if foundID == None:
        #    return {"NOT FOUND":"Can't create Collab if given ID does not exist in USER table"}
        #else:
        cur.execute("INSERT INTO heroku_012605fb848c7a7.collaborators (id, youtube_link) VALUES ('" 
            + id + "', '" 
            + youtube_link + "');")
        mysql.connection.commit()
        posted = {
            'youtube link' : youtube_link,
            'id' : id
        }

        post_log('POST /meals')
        return Response(json.dumps({"posted": posted, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to create this collaborator.", "error message": str(e)}


def getMinID():
    cur = mysql.connection.cursor()
    cur.execute("SELECT max(id) FROM heroku_012605fb848c7a7.collaborators;")
    return cur.fetchone()
