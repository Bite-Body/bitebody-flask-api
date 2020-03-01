from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL

youtube_video = Blueprint("youtube_video", __name__)

from manage import mysql

@youtube_video.route('/all', methods=['GET'])
def get_all_youtube_videos():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * From BiteBody.Youtube_Videos;")
        all_youtube_videos = []
        rows = cur.fetchall()
        for row in rows:
            temp_workout = {}
            temp_workout['id'] = row[0]
            temp_workout['id_collaborator'] = row[1] 
            temp_workout['video_count'] = row[2]
            temp_workout['video_link'] = row[3]
            all_youtube_videos.append(temp_workout)

        return Response(json.dumps({"youtube_videos": all_youtube_videos, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrive all youtube videos."}

@youtube_video.route('/<int:videoID>', methods=['GET'])
def find_Youtube_Videos(videoID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BiteBody.Youtube_Videos WHERE id = "+str(videoID)+";")
        row = cur.fetchone()
        yt_video = {
            'id' : row[0],
            'id_collaborator':row[1],
            'video_count':row[2],
            'video_link' : row[3]
        }
        return Response(json.dumps({"youtube_video": yt_video, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrieve this youtube video."}

@youtube_video.route('/<int:videoID>', methods=['DELETE'])
def delete_youtube_video(videoID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM BiteBody.Youtube_Videos WHERE id = " + str(videoID) + ";")
        mysql.connection.commit()
        deleted = {
            'id' : videoID
        }
        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to delete this youtube video."}

@youtube_video.route('/<int:videoID>', methods = ['PUT'])
def update_youtube_video(videoID):
    try:
        cur = mysql.connection.cursor()
        #id = request.get_json()['id']
        id_collaborator = request.get_json()['id_collaborator']
        video_count = request.get_json()['video_count']
        video_link = request.get_json()['video_link']   
        cur.execute("UPDATE BiteBody.Youtube_Videos SET id = '"+str(videoID) + "',id_collaborator = '" + str(id_collaborator)+ "',video_count = '"+ 
        str(video_count)+"',video_link = '" + str(video_link)+
        "'WHERE id = "+ str(videoID)+";")
        mysql.connection.commit()
        yt_video = { 
            'id': videoID,
            'id_collaborator': id_collaborator,
            'video_count': video_count,
            'video_link' : video_link
        } 
        return Response(json.dumps({"updated": yt_video, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to update this youtube video."}

@youtube_video.route('', methods=['POST'])
def insert_youtube_video():
    try:
        cur = mysql.connection.cursor()
        id = request.get_json()['id']
        id_collaborator = request.get_json()['id_collaborator']
        video_count = request.get_json()['video_count']
        video_link = request.get_json()['video_link']
        cur.execute("INSERT INTO BiteBody.Youtube_Videos (id, id_collaborator, video_count, video_link) VALUES ('" 
            + id + "', '" 
            + id_collaborator + "', '"
            + video_count + "', '" 
            + video_link + "');")
        mysql.connection.commit()
        yt_video = { 
            'id': id,
            'id_collaborator': id_collaborator,
            'video_count': video_count,
            'video_link' : video_link
        }
        return Response(json.dumps({"youtube_video": yt_video, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to create this youtube video."}
