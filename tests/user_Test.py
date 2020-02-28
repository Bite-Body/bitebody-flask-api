import requests
import pprint
import json
#import jfile from 'api/user_Post.json'
#import hector from '../../static/images/HectorBB.png'

def GetAll():
    url = "http://localhost:5000/users/all"

    response = requests.get(url)

    pprint.pprint (response.content)
    pprint.pprint (response.headers)

def GetSingle(userNum):
    url = "http://localhost:5000/users/" + userNum

    res = requests.get(url)
    pprint.pprint (res.content)

def Delete(userNum): #Confirmation Code given despite attempting delete on null row. Figure out Fix
    url = "http://localhost:5000/users/" + userNum

    res = requests.delete(url)
    pprint.pprint (res.content)

def Post():
    #url = "https://reqres.in/api/users"
    url = "http://localhost:5000/users"
    #file = open('C:\\Users\\idavi\\bitebody-flask-api\\api\\user_Post.json', 'r')
    #json_input = file.read()
    #request_json = json.loads(json_input)#parses string back into json format
    #print(request_json)
    response = requests.post(url,data = {"first_name" : "TestFN", "last_name": "TestLN", "email": "TestEmail@Gmail.com" ,"password": "TestPassword"})
    #response = requests.post(url,data = {"name": "Testing WOrld", "job": "Trainer"})
    print(response.text)
   



#print("DISPLAYING ALL USERS")
#GetAll()
#print()
#print()
#userNum = input("WHICH USER DO YOU WANT TO PRINT? INPUT USERNUM")
#GetSingle(userNum)
#userNum = input("WHICH USER DO YOU WANT TO DELETE? INPUT USERNUM")
#Delete(userNum)
Post()


