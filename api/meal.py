from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL
from logger import post_log

meal = Blueprint("meal", __name__)

from manage import mysql

@meal.route('/all', methods=['GET'])
def get_all_meals():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM heroku_012605fb848c7a7.meals;")
        all_meals = []
        rows = cur.fetchall()
        for row in rows:
            temp_meals = {}
            temp_meals['id'] = row[0]
            temp_meals['meal_name'] = row[1] 
            temp_meals['calories'] = row[2]
            temp_meals['protein'] = row[3]
            temp_meals['fat'] = row[4]
            temp_meals['carbs'] = row[5]
            temp_meals['ingredients'] = row[6]
            temp_meals['preptime'] = row[7]
            all_meals.append(temp_meals)

        post_log('GET /meals/all')
        return Response(json.dumps({"meals": all_meals, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrive all meals.", "error message": str(e)}

@meal.route('/<int:meal_ID>', methods=['GET'])
def find_meal(meal_ID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM heroku_012605fb848c7a7.meals WHERE id = "+str(meal_ID)+";")
        row = cur.fetchone()
        meal = {
            'id' : row[0],
            'meal_name':row[1],
            'calories':row[2],
            'protein' : row[3],
            'fat': row[4],
            'carbs': row[5],
            'ingredients': row[6],
            'preptime': row[7]
        }

        post_log('GET /meals/<int:meal_ID>')
        return Response(json.dumps({"meal": meal, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrieve this meal.", "error message": str(e)}

@meal.route('/<int:meal_ID>', methods=['DELETE'])
def delete_meal(meal_ID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM heroku_012605fb848c7a7.meals WHERE id = " + str(meal_ID) + ";")
        mysql.connection.commit()
        deleted = {
            'id' : meal_ID
        }

        post_log('DELETE /meals/<int:meal_ID>')
        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to delete this meal.", "error message": str(e)}

@meal.route('/<int:meal_ID>', methods = ['PUT'])
def update_meal_info(meal_ID):
    try:
        cur = mysql.connection.cursor()
        id = request.get_json()['id']
        meal_name = request.get_json()['meal_name']
        calories = request.get_json()['calories']
        protein = request.get_json()['protein']
        fat = request.get_json()['fat']
        carbs = request.get_json()['carbs']
        ingredients = request.get_json()['ingredients']
        preptime = request.get_json()['preptime']
        cur.execute("UPDATE heroku_012605fb848c7a7.meals SET meal_name = '"+str(meal_name) + "',calories = '" + str(calories)+ "',protein = '"+ 
        str(protein)+"',fat = '"+ str(fat) + "',carbs = '" + str(carbs)+"',ingredients = '" + str(ingredients)+"',preptime = '" + str(preptime)+
        "'WHERE id = "+ str(meal_ID)+";")
        mysql.connection.commit()
        meal = { 
            'id' : meal_ID,
            'meal_name': meal_name,
            'calories': calories,
            'protein' : protein,
            'fat': fat,
            'carbs': carbs,
            'ingredients': ingredients,
            'preptime': preptime                
        }

        post_log('PUT /meals/<int:meal_ID>')
        return Response(json.dumps({"updated": meal, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to update this meal.", "error message": str(e)}

@meal.route('', methods=['POST'])
def insert_meal():
    try:
        cur = mysql.connection.cursor()
        id = request.get_json()['id']
        meal_name = request.get_json()['meal_name']
        calories = request.get_json()['calories']
        protein = request.get_json()['protein']
        fat = request.get_json()['fat']
        carbs = request.get_json()['carbs']
        ingredients = request.get_json()['ingredients']
        preptime = request.get_json()['preptime']
        cur.execute("INSERT INTO heroku_012605fb848c7a7.meals (id, meal_name, calories, protein, fat, carbs, ingredients, preptime) VALUES ('" 
            + id + "', '" 
            + meal_name + "', '" 
            + calories + "', '" 
            + protein + "', '"
            + fat + "', '"  
            + carbs + "', '" 
            + ingredients + "', '" 
            + preptime + "');")
        mysql.connection.commit()
        meal = { 
            'id' : id,
            'meal_name': meal_name,
            'calories': calories,
            'protein' : protein,
            'fat': fat,
            'carbs': carbs,
            'ingredients': ingredients,
            'preptime': preptime                
        }

        post_log('POST /meals')
        return Response(json.dumps({"meal added": meal, "code": 201}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to create this meal.", "error message": str(e)}
