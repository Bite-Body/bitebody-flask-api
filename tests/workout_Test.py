import requests
import request
import pprint
import json

#import jfile from 'api/user_Post.json'
#import hector from '../../static/images/HectorBB.png'

def GetAll():
    url = "https://gentle-inlet-25364.herokuapp.com/workouts/all"

    response = requests.get(url)
    pprint.pprint (response.text)


    if "code" in response.text:
        print("GET ALL Passed")
        global pc
        pc =  pc + 1
        return pc
    else:
        print("GET ALL Failed")

def GetSingle(userNum):
    url = "https://gentle-inlet-25364.herokuapp.com/workouts/" + userNum

    res = requests.get(url)
    pprint.pprint (res.content)

    if "code" in res.text:
        print("GET SINGLE Passed")
        global pc
        pc = pc + 1
        return pc
    else:
        print("GET SINGLE Failed")

def Delete(userNum): #Confirmation Code given despite attempting delete on null row. Figure out Fix
    url = "https://gentle-inlet-25364.herokuapp.com/workouts/" + userNum

    res = requests.delete(url)
    pprint.pprint (res.content)
    if "code" in res.text:
        print("DELETE Passed")
        global pc
        pc = pc + 1
        return pc
    else:
        print("DELETE Failed")

def Post():
    url = "https://gentle-inlet-25364.herokuapp.com/workouts"
    payload = {"id" : "10",
    "workout_name":"test", 
    "workout_description": "test",
    "workout_image_path": "test", 
    "genre":"test", 
    "body_part":"test",
    "duration": "test",
    "equipment": "test" }
    r = requests.post(url, json=payload)
    print(r)
    print(r.text)
    if "code" in r.text:
        print("POST Passed")
        global pc
        pc = pc + 1
        return pc
    else:
        print("POST Failed")


def Put(userNum):
    url = "https://gentle-inlet-25364.herokuapp.com/workouts/" + userNum
    payload = {
    "workout_name":"updated", 
    "workout_description": "updated",
    "workout_image_path": "updated", 
    "genre":"updated", 
    "body_part":"updated",
    "duration": "updated",
    "equipment": "updated"}
    r = requests.put(url, json=payload)
    print(r)
    print(r.text)
    if "code" in r.text:
        print("PUT Passed")
        global pc
        pc = pc + 1
        return pc
    else:
        print("PUT Failed")
    


pc = 0
GetAll()
GetSingle("1")
Delete("10")
Post()
Put("10")
print(pc , "/5 tests passed")