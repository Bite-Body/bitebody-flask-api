import requests
import request
import pprint
import json
from logger import post_log

def calc_test(): 
    url = "https://gentle-inlet-25364.herokuapp.com/calories/"
    
    payload = {"age":"37", "gender":"male", "weigth": "180", "height": "76", "activity": "light", "goal": "gain", "gain": "2"}
    r = requests.post(url, json=payload)
    print(r)
    print(r.text)
    if "code" in r.text:
        print("POST Passed")
        global caloriesPC
        mealPC = caloriesPC + 1
        return caloriesPC
        post_log('Calorie Calc')
    else:
        print("calories Failed")