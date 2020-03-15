import requests
import pprint
import json

import collab


#import jfile from 'api/user_Post.json'
#import hector from '../../static/images/HectorBB.png'

def GetAll():
    url = "https://gentle-inlet-25364.herokuapp.com/collabs/all"

    response = requests.get(url)

    pprint.pprint (response.text)


    if "code" in response.text:
        print("GET ALL Passed")
        global collabPC
        collabPC =  collabPC + 1
        return collabPC
    else:
        print("GET ALL Failed")

def GetSingle(userNum):
    url = "https://gentle-inlet-25364.herokuapp.com/collabs/" + userNum

    res = requests.get(url)
    pprint.pprint (res.content)

    if "code" in res.text:
        print("GET SINGLE Passed")
        global collabPC
        collabPC = collabPC + 1
        return collabPC
    else:
        print("GET SINGLE Failed")

def Delete(): #Confirmation Code given despite attempting delete on null row. Figure out Fix
    userNum = collab.getMinID()
    url = "https://gentle-inlet-25364.herokuapp.com/collabs/" + userNum

    res = requests.delete(url)
    pprint.pprint (res.content)
    if "code" in res.text:
        print("DELETE Passed")
        global collabPC
        collabPC = collabPC + 1
        return collabPC
    else:
        print("DELETE Failed")

def Post():
    url = "https://gentle-inlet-25364.herokuapp.com/collabs"
    payload = {"id" : "50","youtube_link":"www.youtube.com/test"}
    r = requests.post(url, json=payload)
    print(r)
    print(r.text)
    if "code" in r.text:
        print("POST Passed")
        global collabPC
        collabPC = collabPC + 1
        return collabPC
    else:
        print("POST Failed")


def Put(userNum):
    url = "https://gentle-inlet-25364.herokuapp.com/collabs/" + userNum
    payload = {"youtube_link": "www.youtube.com/test_updated"}
    r = requests.put(url, json=payload)
    print(r)
    print(r.text)
    if "code" in r.text:
        print("PUT Passed")
        global collabPC
        collabPC = collabPC + 1
        return collabPC
    else:
        print("PUT Failed")
    


collabPC = 0
