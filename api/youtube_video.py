from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL
from logger import post_log

youtube_video = Blueprint("youtube_video", __name__)

from manage import mysql

@youtube_video.route('/all', methods=['GET'])
def get_all_youtube_videos():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * From heroku_012605fb848c7a7.youtube_videos;")
        all_youtube_videos = []
        rows = cur.fetchall()
        for row in rows:
            temp_workout = {}
            temp_workout['id'] = row[0]
            temp_workout['id_collaborator'] = row[1] 
            temp_workout['video_count'] = row[2]
            temp_workout['video_link'] = row[3]
            all_youtube_videos.append(temp_workout)

        post_log('GET /youtube_videos/all')
        return Response(json.dumps({"youtube_videos": all_youtube_videos, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrive all youtube videos."}

@youtube_video.route('/<int:videoID>', methods=['GET'])
def find_Youtube_Videos(videoID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM heroku_012605fb848c7a7.youtube_videos WHERE id = "+str(videoID)+";")
        row = cur.fetchone()
        yt_video = {
            'id' : row[0],
            'id_collaborator':row[1],
            'video_count':row[2],
            'video_link' : row[3]
        }

        post_log('GET /youtube_videos/<int:videoID>')
        return Response(json.dumps({"youtube_video": yt_video, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrieve this youtube video."}

@youtube_video.route('/<int:videoID>', methods=['DELETE'])
def delete_youtube_video(videoID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM heroku_012605fb848c7a7.youtube_videos WHERE id = " + str(videoID) + ";")
        mysql.connection.commit()
        deleted = {
            'id' : videoID
        }

        post_log('DELETE /youtube_videos/<int:videoID>')
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
        cur.execute("UPDATE heroku_012605fb848c7a7.youtube_videos SET id = '"+str(videoID) + "',id_collaborator = '" + str(id_collaborator)+ "',video_count = '"+ 
        str(video_count)+"',video_link = '" + str(video_link)+
        "'WHERE id = "+ str(videoID)+";")
        mysql.connection.commit()
        yt_video = { 
            'id': videoID,
            'id_collaborator': id_collaborator,
            'video_count': video_count,
            'video_link' : video_link
        }

        post_log('PUT /youtube_videos/<int:videoID>') 
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
        cur.execute("INSERT INTO heroku_012605fb848c7a7.youtube_videos (id, id_collaborator, video_count, video_link) VALUES ('" 
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

        post_log('POST /youtube_videos')
        return Response(json.dumps({"youtube_video": yt_video, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to create this youtube video."}
