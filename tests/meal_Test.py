import requests
import request
import pprint
import json

#import jfile from 'api/user_Post.json'
#import hector from '../../static/images/HectorBB.png'


def GetAll():
    url = "https://gentle-inlet-25364.herokuapp.com/meals/all"

    response = requests.get(url)

    pprint.pprint (response.text)


    if "code" in response.text:
        print("GET ALL Passed")
        global mealPC
        mealPC =  mealPC + 1
        return mealPC
    else:
        print("GET ALL Failed")

def GetSingle(userNum):
    url = "https://gentle-inlet-25364.herokuapp.com/meals/" + userNum

    res = requests.get(url)
    pprint.pprint (res.content)

    if "code" in res.text:
        print("GET SINGLE Passed")
        global mealPC
        mealPC = mealPC + 1
        return mealPC
    else:
        print("GET SINGLE Failed")

def Delete(userNum): #Confirmation Code given despite attempting delete on null row. Figure out Fix
    url = "https://gentle-inlet-25364.herokuapp.com/meals/" + userNum
    res = requests.delete(url)
    pprint.pprint (res.content)
    if "code" in res.text:
        print("DELETE Passed")
        global mealPC
        mealPC = mealPC + 1
        return mealPC
    else:
        print("DELETE Failed")

def Post():
    url = "https://gentle-inlet-25364.herokuapp.com/meals"

    payload = {"id":"11", "meal_name":"testMeal", "calories": "0", "protein": "testProtein", "fat": "testFat", "carbs": "testCarbs", "ingredients": "testIngredients", "preptime": "testPreptime", "directions": "testDirections", "image_path": "testImage", "breakfast": "0", "lunch": "0", "dinner": "0", "brunch": "0", "linner":"0"}
    r = requests.post(url, json=payload)
    print(r)
    print(r.text)
    if "code" in r.text:
        print("POST Passed")
        global mealPC
        mealPC = mealPC + 1
        return mealPC
    else:
        print("POST Failed")


def Put(userNum):
    url = "https://gentle-inlet-25364.herokuapp.com/meals/" + userNum
    payload = {"id":"11", "meal_name":"updated", "calories": "updated", "protein": "updated", "fat": "updated", "carbs": "updated", "ingredients": "updated", "preptime": "updated", "directions": "updated", "image_path": "updated", "breakfast": "u", "lunch": "u", "dinner": "u", "brunch": "u", "linner":"u"}
    r = requests.put(url, json=payload)
    print(r)
    print(r.text)
    if "code" in r.text:
        print("PUT Passed")
        global mealPC
        mealPC = mealPC + 1
        return mealPC
    else:
        print("PUT Failed")
    


mealPC = 0


