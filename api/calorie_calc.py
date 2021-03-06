from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL
from logger import post_log

calorie_calc = Blueprint("calorie_calc", __name__)

from manage import mysql

@calorie_calc.route('', methods=['POST'])
def calc_cal():
    try:
        def user_info():
            age = request.get_json()['age']
            gender = request.get_json()['gender']
            weight = request.get_json()['weight']
            height = request.get_json()['height']

            if gender == 'male':
                c1 = 66
                hm = 5 * height
                wm = 12.7 * weight
                am = 6.7 * age
            elif gender == 'female':
                c1 = 655
                hm = 2 * height
                wm = 9.5 * weight
                am = 4.7 * age

            #BMR = Basal Metabolic Rate Formulas
            bmr_result = c1 + hm + wm - am
            return(int(bmr_result))

        def calculate_activity(bmr_result): 
            activity_level = request.get_json()['activity']

            if activity_level == 'none':
                activity_level = 1.2 * bmr_result
            elif activity_level == 'light':
                activity_level = 1.375 * bmr_result
            elif activity_level == 'moderate':
                activity_level = 1.55 * bmr_result
            elif activity_level == 'high':
                activity_level = 1.725 * bmr_result
            
            return(int(activity_level))

        def gain_or_lose(activity_level):
            goals = request.get_json()['goal']
            
            if goals == 'lose':
                calories = activity_level - 500
            elif goals == 'maintain':
                calories = activity_level
            elif goals == 'gain':
                calories = activity_level + 500
            
            return int(calories)


        cal_count = gain_or_lose(calculate_activity(user_info()))

        post_log('GET /calories')
        return Response(json.dumps({"Daily calorie to consume": cal_count, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to calculate calories.", "error message": str(e), "payload sent": request.get_json()}
