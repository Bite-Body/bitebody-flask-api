from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL

calorie_calc = Blueprint("calorie_calc", __name__)

from manage import mysql

@app.route('', methods=['POST'])
def calorie_calc():
    try:
        def user_info():
            age = int(input('What is your age: '))
            gender = input('What is your gender: ')
            weight = int(input('What is your weight: '))
            height = int(input('What is your height in inches: '))

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
            activity_level = input('What is your activity level (none, light, moderate, or high): ')

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
            goals = input('Do you want to lose, maintain, or gain weight: ')

            if goals == 'lose':
                calories = activity_level - 500
            elif goals == 'maintain':
                calories = activity_level
            elif goals == 'gain':
                gain = int(input('Gain 1 or 2 pounds per week? Enter 1 or 2: '))
                if gain == 1: 
                    calories = activity_level + 500
                elif gain == 2:
                    calories = activity_level + 1000

            print('in order to ', goals, 'weight, your daily caloric goals should be', int(calories), '!')

        return Response(json.dumps({"Daily calorie to consume": gain_or_lose(calculate_activity(user_info())), "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to calculate calories."}