import requests
import request
import pprint
import json

#import jfile from 'api/user_Post.json'
#import hector from '../../static/images/HectorBB.png'

def GetAll():
    url = "https://gentle-inlet-25364.herokuapp.com/youtube_videos/all"

    response = requests.get(url)

    pprint.pprint (response.text)


    if "code" in response.text:
        print("GET ALL Passed")
        global youtubePC
        youtubePC =  youtubePC + 1
        return youtubePC
    else:
        print("GET ALL Failed")

def GetSingle(userNum):
    url = "https://gentle-inlet-25364.herokuapp.com/youtube_videos/" + userNum

    res = requests.get(url)
    pprint.pprint (res.content)

    if "code" in res.text:
        print("GET SINGLE Passed")
        global youtubePC
        youtubePC = youtubePC + 1
        return youtubePC
    else:
        print("GET SINGLE Failed")

def Delete(userNum): #Confirmation Code given despite attempting delete on null row. Figure out Fix
    url = "https://gentle-inlet-25364.herokuapp.com/youtube_videos/" + userNum

    res = requests.delete(url)
    pprint.pprint (res.content)
    if "code" in res.text:
        print("DELETE Passed")
        global youtubePC
        youtubePC = youtubePC + 1
        return youtubePC
    else:
        print("DELETE Failed")

def Post():
    url = "https://gentle-inlet-25364.herokuapp.com/youtube_videos"
    payload = {"id" : "50","id_collaborator":"1", "video_count":"test", "video_link":"test"}
    r = requests.post(url, json=payload)
    print(r)
    print(r.text)
    if "code" in r.text:
        print("POST Passed")
        global youtubePC
        youtubePC = youtubePC + 1
        return youtubePC
    else:
        print("POST Failed")


def Put(userNum):
    url = "https://gentle-inlet-25364.herokuapp.com/youtube_videos/" + userNum
    payload = {"id_collaborator":"28", "video_count":"update", "video_link":"update"}
    r = requests.put(url, json=payload)
    print(r)
    print(r.text)
    if "code" in r.text:
        print("PUT Passed")
        global youtubePC
        youtubePC = youtubePC + 1
        return youtubePC
    else:
        print("PUT Failed")
    


youtubePC = 0
