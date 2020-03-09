import requests
import request
import pprint
import json

#import jfile from 'api/user_Post.json'
#import hector from '../../static/images/HectorBB.png'


def GetAll():
    url = "https://gentle-inlet-25364.herokuapp.com/users/all"

    response = requests.get(url)

    pprint.pprint (response.text)

    if "code" in response.text:
        print("GET ALL Passed")
        global pc
        pc =  pc + 1
        return pc
    else:
        print("GET ALL Failed")
    #pprint.pprint (response.headers)

def GetSingle(userNum):
    url = "https://gentle-inlet-25364.herokuapp.com/users/" + userNum

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
    url = "https://gentle-inlet-25364.herokuapp.com/users/" + userNum

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
    #url = "https://reqres.in/api/users"
    url = "https://gentle-inlet-25364.herokuapp.com/users"

    #MISCELLANEOUS WORK TOWARDS BUG FIXING AND OTHER API TESTING

    #file = open('C:\\Users\\idavi\\bitebody-flask-api\\api\\user_Post.json', 'r')
    #json_input = file.read()
    #request_json = json.loads(json_input)#parses string back into json format
    #print(request_json)
    #response = requests.post(url,data = {"first_name" : "TestFN", "last_name": "TestLN", "email": "TestEmail@Gmail.com" ,"password": "TestPassword"})
    #response = requests.post(url,data = {"name": "Testing WOrld", "job": "Trainer"})
    #print(response.text)
   
    #METHOD 1 -- FAULTY
    #url = "http://localhost:5000/users"
    #response = requests.post(url,data = {"first_name" : "TestFN", "last_name": "TestLN", "email": "TestEmail@Gmail.com" ,"password": "TestPassword"})
    #print(response.text)

    ##METHOD 2 -- FAULTY
    #file = open('C:\\Users\\idavi\\bitebody-flask-api\\api\\user_Post.json', 'r')
    #json_input = file.read()
    #request_json = json.loads(json_input)#parses string back into json format
    #response = requests.post(url,request_json)
    #print(request_json)
    #print(response.text)

    ##METHOD 3 -- FAULTY
    #with open('C:\\Users\\idavi\\bitebody-flask-api\\api\\user_Post.json') as json_file:
        #data = json.load(json_file)
        #print(data)
        #response = requests.post(url,data)
        #print(response.text)

    ##METHOD 4 -- ACTUALLY WORKS (THANK THE LORD)
    payload = {"first_name" : "TestFN", "last_name": "TestLN", "email": "TestEmail@Gmail.com" ,"password": "TestPassword"}
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
    url = "https://gentle-inlet-25364.herokuapp.com/users/" + userNum
    payload = {"first_name" : "UpdatedFN", "last_name": "UpdatedLN", "email": "UpdatedEmail@Gmail.com" ,"password": "UpdatedPassword"}
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

def PostLogin():
    url = "https://gentle-inlet-25364.herokuapp.com/users/login"
    payload = {"email": "TestEmail@Gmail.com", "password": "TestPassword"}
    r = requests.post(url, json = payload)
    print(r)
    print(r.text)
    if "yes" in r.text:
        print("POSTLOGIN Passed")
        global pc
        pc = pc + 1
        return pc
    else:
        print("POSTLOGIN Failed")
    


pc = 0
GetAll()
GetSingle("1")
Post()
Delete("1")
Put("1")
PostLogin()
print(pc , "/6 tests passed")

