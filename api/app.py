from flask import Flask, Response, jsonify, json, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')

app.config['MYSQL_HOST'] = 'mysql-db.ck7dyilntvz9.us-west-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'f*ckthisdb69'
app.config['MYSQL_DB'] = 'BiteBody'

mysql = MySQL(app)

CORS(app)

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

#-----------------------USER-METHODS-START----------------------#
@app.route('/users/all', methods=['GET'])
def get_all_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM BiteBody.Users;")

    all_users = []

    rows = cur.fetchall()

    for row in rows:
        temp_user = {}
        temp_user['id'] = row[0]
        temp_user['first_name'] = row[1]
        temp_user['last_name'] = row[2]
        temp_user['email'] = row[3]
        # temp_user['password'] = row[4] don't send this lol
        all_users.append(temp_user)

    # https://stackoverflow.com/questions/29020839/mysql-fetchall-how-to-get-data-inside-a-dict-rather-than-inside-a-tuple
    # These two lines zips the resulting values with cursor.description
    # columns = [col[0] for col in cur.description]
    # rows = [dict(zip(columns, row)) for row in cur.fetchall()]

    return Response(json.dumps({"users": all_users, "code": 200}), mimetype='application/json')

@app.route('/users/<int:userID>', methods=['DELETE'])
def delete_user(userID):
    try:
        cur = mysql.connection.cursor()


        cur.execute("DELETE FROM BiteBody.Users WHERE id = " + str(userID) + ";")
        mysql.connection.commit()

        deleted = {
            'id' : userID
        }

        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}

@app.route('/users', methods=['POST'])
def create_user():
    cur = mysql.connection.cursor()

    print(request.get_json())

    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    while((email.find('@') == -1)):
        print('Inavalid email please enter again?\n')
        email = input('Inavalid email please enter again?\n')

    password = request.get_json()['password']
    while (len(password) < 7):
        print('password is too weak please add more characters')
        password = input('Enter new password\n')

    cur.execute("INSERT INTO BiteBody.Users (first_name, last_name, email, password) VALUES ('" 
        + first_name + "', '" 
        + last_name + "', '" 
        + email + "', '" 
        + password + "');")

    mysql.connection.commit()

    posted = {
		'first_name' : first_name,
		'last_name' : last_name,
		'email' : email,
		'password' : password
	}
    
    return Response(json.dumps({"posted": posted, "code": 201}), mimetype='application/json')

@app.route('/users/<int:userID>', methods = ['PUT'])
def update_user_info(userID):
    try:
        cur = mysql.connection.cursor()
        first_name = request.get_json()['first_name']
        last_name = request.get_json()['last_name']
        email = request.get_json()['email']
        password = request.get_json()['password']
            

        cur.execute("UPDATE BiteBody.Users SET first_name = '"+str(first_name) + "',last_name = '" + str(last_name)+ "',email = '"+ str(email)+"',password = '"+ str(password) + 
        "'WHERE id = "+ str(userID)+";")
        mysql.connection.commit()
        updated = {
                'first_name':first_name,
                'last_name':last_name,
                'email' : email,
                'password' : password
            }
            

        return Response(json.dumps({"updated": updated, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}

@app.route('/users/<int:userID>', methods=['GET'])
def find_user(userID):
    try:
        cur = mysql.connection.cursor()
        

        cur.execute("SELECT * FROM BiteBody.Users WHERE id = "+str(userID)+";")
        row = cur.fetchone()
        
        user = {
                'first_name':row[1],
                'last_name':row[2],
                'email' : row[3],
                'id' : row[0]
            }

        

        return Response(json.dumps({"user": user, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}

@app.route('/users/login', methods=['POST'])
def login():
    try:
        cur = mysql.connection.cursor()
        email = request.get_json()['email']
        password = request.get_json()['password']
        
        
        while((email.find('@') == -1)):
            print('Inavalid email please enter again?\n')
            email = input('Inavalid email please enter again?\n')
        
        cur.execute("SELECT * FROM BiteBody.Users where email = '" + str(email) + "'")
        rv = cur.fetchone()
        
        if (rv[4] == password):
            
            print("Password Match")
        else:
            print("Password not matching")
        
        return {"error": "nah"}
    except Exception as e:
        print(e)
        return {"error": "yep"}

#-----------------------USER-METHODS-END----------------------#

        ##COLLABORATOR table endpoints

#---------------------Collaborator-Endpoints-Start---------------------#       
@app.route('/collabs/all', methods=['GET'])
def get_all_collabs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM BiteBody.Collaborators;")

    all_collabs = []

    rows = cur.fetchall()

    for row in rows:
        temp_collab = {}
        temp_collab['id'] = row[0]
        temp_collab['youtube_link'] = row[1]
        all_collabs.append(temp_collab)

    # https://stackoverflow.com/questions/29020839/mysql-fetchall-how-to-get-data-inside-a-dict-rather-than-inside-a-tuple
    # These two lines zips the resulting values with cursor.description
    # columns = [col[0] for col in cur.description]
    # rows = [dict(zip(columns, row)) for row in cur.fetchall()]

    return Response(json.dumps({"users": all_collabs, "code": 404}), mimetype='application/json')



@app.route('/collabs/<int:collabID>', methods=['GET'])
def find_collaborator(collabID):
    try:
        cur = mysql.connection.cursor()
        

        cur.execute("SELECT * FROM BiteBody.Collaborators WHERE id = "+str(collabID)+";")
        row = cur.fetchone()
        
        collab = {
                'youtube_link':row[1],
                'id' : row[0]
            }

        

        return Response(json.dumps({"collaborator": collab, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}



@app.route('/collabs', methods=['POST'])
def create_collab():
    cur = mysql.connection.cursor()

    print(request.get_json())

    id = request.get_json()['id']
    youtube_link = request.get_json()['youtube_link']

    cur.execute("INSERT INTO BiteBody.Collaborators (id, youtube_link) VALUES ('" 
        + id + "', '" 
        + youtube_link + "');")

    mysql.connection.commit()

    posted = {
		'youtube link' : youtube_link,
		'id' : id
	}
    
    return Response(json.dumps({"posted": posted, "code": 201}), mimetype='application/json')


@app.route('/collabs/<int:collabID>', methods = ['PUT'])
def update_collab_info(collabID):
    try:
        cur = mysql.connection.cursor()

        youtube_link = request.get_json()['youtube_link']
            

        cur.execute("UPDATE BiteBody.Collaborators SET youtube_link = '"+str(youtube_link) + 
        "'WHERE id = "+ str(collabID)+";")
        mysql.connection.commit()
        updated = {
                'youtube_link':youtube_link
            }
            

        return Response(json.dumps({"updated": updated, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}


@app.route('/collabs/<int:collabID>', methods=['DELETE'])
def delete_collab(collabID):
    try:
        cur = mysql.connection.cursor()


        cur.execute("DELETE FROM BiteBody.Collaborators WHERE id = " + str(collabID) + ";")
        mysql.connection.commit()

        deleted = {
            'id' : collabID
        }

        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}

        ##COLLABORATOR table endpoints
        #David's Contributions WOAH
#---------------------Collaborator-Endpoints-End---------------------# 


#---------------------Workout-Endpoints-Start---------------------# 
#GET ALL WORKOUTS
@app.route('/workouts/all', methods = ['GET'])
def get_all_workouts():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * From BiteBody.Workouts;")

        all_workouts = []

        rows = cur.fetchall()

        for row in rows:
            temp_workout = {}
            temp_workout['id'] = row[0]
            temp_workout['wkout_name'] = row[1] 
            temp_workout['wkout_description'] = row[2]
            temp_workout['wkout_image_path'] = row[3]
            temp_workout['genre'] = row[4]
            temp_workout['body_part'] = row[5]
            temp_workout['duration'] = row[6]
            temp_workout['equipment'] = row[7]
            all_workouts.append(temp_workout)
            

        
            

        return Response(json.dumps({"workouts": all_workouts, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yes"}

#GET SPECIFIC WORKOUTS
@app.route('/workouts/<int:wkoutID>', methods=['GET'])
def find_workout(wkoutID):
    try:
        cur = mysql.connection.cursor()
        

        cur.execute("SELECT * FROM BiteBody.Workouts WHERE wkout_ID = "+str(wkoutID)+";")
        row = cur.fetchone()
        
        workout = {
                'id' : row[0],
                'Workout_name':row[1],
                'workout_description':row[2],
                'workout_image_path' : row[3],
                'Genre': row[4],
                'body_part': row[5],
                'duration': row[6],
                'equipment': row[7]
                
            }

        

        return Response(json.dumps({"workout": workout, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}
#ADD A WORKOUT
@app.route('/workouts', methods=['POST'])
def insert_workout():
    cur = mysql.connection.cursor()

    print(request.get_json())

    wkout_ID = request.get_json()['wkout_ID']
    wkout_name = request.get_json()['wkout_name']
    wkout_description = request.get_json()['wkout_description']
    wkout_image_path = request.get_json()['wkout_image_path']
    genre = request.get_json()['genre']
    body_part = request.get_json()['body_part']
    duration = request.get_json()['duration']
    equipment = request.get_json()['equipment']

    cur.execute("INSERT INTO BiteBody.Workouts (wkout_ID, wkout_name, wkout_description, wkout_image_path, genre, body_part, duration, equipment) VALUES ('" 
        + wkout_ID + "', '" 
        + wkout_name + "', '" 
        + wkout_description + "', '" 
        + wkout_image_path + "', '"
        + genre + "', '"  
        + body_part + "', '" 
        + duration + "', '" 
        + equipment + "');")

    mysql.connection.commit()

    workout = { 
                'wkout_ID': wkout_ID,
                'wkout_name': wkout_name,
                'wkout_description': wkout_description,
                'wkout_image_path' : wkout_image_path,
                'Genre': genre,
                'body_part': body_part,
                'duration': duration,
                'equipment': equipment
                
            }
    
    return Response(json.dumps({"workout added": workout, "code": 201}), mimetype='application/json')

#UPDATE A WORKOUT
@app.route('/workouts/<int:wkoutID>', methods = ['PUT'])
def update_workout_info(wkoutID):
    try:
        cur = mysql.connection.cursor()
        wkout_name = request.get_json()['wkout_name']
        wkout_description = request.get_json()['wkout_description']
        wkout_image_path = request.get_json()['wkout_image_path']
        genre = request.get_json()['genre']
        body_part = request.get_json()['body_part']
        duration = request.get_json()['duration']
        equipment = request.get_json()['equipment']
            

        cur.execute("UPDATE BiteBody.Workouts SET wkout_name = '"+str(wkout_name) + "',wkout_description = '" + str(wkout_description)+ "',wkout_image_path = '"+ 
        str(wkout_image_path)+"',genre = '"+ str(genre) + "',body_part = '" + str(body_part)+"',duration = '" + str(duration)+"',equipment = '" + str(equipment)+
        "'WHERE wkout_ID = "+ str(wkoutID)+";")
        mysql.connection.commit()
        workout = { 
                'wkout_ID': wkoutID,
                'wkout_name': wkout_name,
                'wkout_description': wkout_description,
                'wkout_image_path' : wkout_image_path,
                'Genre': genre,
                'body_part': body_part,
                'duration': duration,
                'equipment': equipment
                
            }
            

        return Response(json.dumps({"updated": workout, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}

#DELETE WORKOUT
@app.route('/workouts/<int:wkoutID>', methods=['DELETE'])
def delete_workout(wkoutID):
    try:
        cur = mysql.connection.cursor()


        cur.execute("DELETE FROM BiteBody.Workouts WHERE wkout_ID = " + str(wkoutID) + ";")
        mysql.connection.commit()

        deleted = {
            'id' : wkoutID
        }

        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}
#---------------------WORKOUTS-ENDPOINTS-END---------------------# 


#---------------------Youtube-Endpoints-Start---------------------# 
#GET ALL YOUTUBE VIDEOS
@app.route('/youtube_videos/all', methods = ['GET'])
def get_all_youtube_videos():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * From BiteBody.Youtube_Videos;")

        all_youtube_videos = []

        rows = cur.fetchall()

        for row in rows:
            temp_workout = {}
            temp_workout['video_id'] = row[0]
            temp_workout['collab_id'] = row[1] 
            temp_workout['video_count'] = row[2]
            temp_workout['video_link'] = row[3]
            all_youtube_videos.append(temp_workout)

        return Response(json.dumps({"youtube_videos": all_youtube_videos, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yes"}

#GET SPECIFIC YOUTUBE VIDEO
@app.route('/youtube_videos/<int:videoID>', methods=['GET'])
def find_Youtube_Videos(videoID):
    try:
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM BiteBody.Youtube_Videos WHERE video_ID = "+str(videoID)+";")
        row = cur.fetchone()
        
        yt_video = {
            'video_id' : row[0],
            'collab_id':row[1],
            'video_count':row[2],
            'video_link' : row[3]
        }

        return Response(json.dumps({"youtube_video": yt_video, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}

#ADD A YOUTUBE VIDEO
@app.route('/youtube_videos', methods=['POST'])
def insert_youtube_video():
    cur = mysql.connection.cursor()

    video_id = request.get_json()['video_id']
    collab_id = request.get_json()['collab_id']
    video_count = request.get_json()['video_count']
    video_link = request.get_json()['video_link']

    cur.execute("INSERT INTO BiteBody.Youtube_Videos (video_ID, collaborator_ID, video_count, video_link) VALUES ('" 
        + video_id + "', '" 
        + collab_id + "', '"
        + video_count + "', '" 
        + video_link + "');")

    mysql.connection.commit()

    yt_video = { 
        'video_id': video_id,
        'collab_id': collab_id,
        'video_count': video_count,
        'video_link' : video_link
    }
    
    return Response(json.dumps({"youtube_video": yt_video, "code": 201}), mimetype='application/json')

#UPDATE A YOUTUBE VIDEO
@app.route('/youtube_videos/<int:videoID>', methods = ['PUT'])
def update_youtube_video(videoID):
    try:
        cur = mysql.connection.cursor()

        video_id = request.get_json()['video_id']
        collab_id = request.get_json()['collab_id']
        video_count = request.get_json()['video_count']
        video_link = request.get_json()['video_link']   

        cur.execute("UPDATE BiteBody.Youtube_Videos SET video_ID = '"+str(video_id) + "',collaborator_ID = '" + str(collab_id)+ "',video_count = '"+ 
        str(video_count)+"',video_link = '" + str(video_link)+
        "'WHERE video_ID = "+ str(videoID)+";")
        mysql.connection.commit()

        yt_video = { 
            'video_id': video_id,
            'collab_id': collab_id,
            'video_count': video_count,
            'video_link' : video_link
        } 

        return Response(json.dumps({"updated": yt_video, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}

#DELETE A YOUTUBE VIDEO
@app.route('/youtube_videos/<int:videoID>', methods=['DELETE'])
def delete_youtube_video(videoID):
    try:
        cur = mysql.connection.cursor()

        cur.execute("DELETE FROM BiteBody.Youtube_Videos WHERE video_ID = " + str(videoID) + ";")
        mysql.connection.commit()

        deleted = {
            'id' : videoID
        }

        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yep"}
#---------------------YOUTUBE VIDEO-ENDPOINTS-END---------------------# 


#---------------------MEALS-ENDPOINTS-START---------------------#

#GET ALL MEALS
@app.route('/meals/all', methods = ['GET'])
def get_all_meals():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BiteBody.Meals;")

        all_meals = []

        rows = cur.fetchall()

        for row in rows:
            temp_meals = {}
            temp_meals['meal_ID'] = row[0]
            temp_meals['meal_name'] = row[1] 
            temp_meals['calories'] = row[2]
            temp_meals['protein'] = row[3]
            temp_meals['fat'] = row[4]
            temp_meals['carbs'] = row[5]
            temp_meals['ingredients'] = row[6]
            temp_meals['preptime'] = row[7]
            all_meals.append(temp_meals)





        return Response(json.dumps({"meals": all_meals, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yes"}


#GET SPECIFIC Meals
@app.route('/meals/<int:meal_ID>', methods=['GET'])
def find_meal(meal_ID):
    try:
        cur = mysql.connection.cursor()


        cur.execute("SELECT * FROM BiteBody.Meals WHERE id = "+str(meal_ID)+";")
        row = cur.fetchone()

        meal = {
                'meal_ID' : row[0],
                'meal_name':row[1],
                'calories':row[2],
                'protein' : row[3],
                'fat': row[4],
                'carbs': row[5],
                'ingredients': row[6],
                'preptime': row[7]

            }



        return Response(json.dumps({"meal": meal, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yes"}


#ADD A MEAL
@app.route('/meals', methods=['POST'])
def insert_meal():
    cur = mysql.connection.cursor()

    print(request.get_json())

    meal_ID = request.get_json()['meal_ID']
    meal_name = request.get_json()['meal_name']
    calories = request.get_json()['calories']
    protein = request.get_json()['protein']
    fat = request.get_json()['fat']
    carbs = request.get_json()['carbs']
    ingredients = request.get_json()['ingredients']
    preptime = request.get_json()['preptime']

    cur.execute("INSERT INTO BiteBody.Meals (meal_ID, meal_name, calories, protein, fat, carbs, ingredients, preptime) VALUES ('" 
        + meal_ID + "', '" 
        + meal_name + "', '" 
        + calories + "', '" 
        + protein + "', '"
        + fat + "', '"  
        + carbs + "', '" 
        + ingredients + "', '" 
        + preptime + "');")

    mysql.connection.commit()

    meal = { 
                'meal_ID' : meal_ID,
                'meal_name': meal_name,
                'calories': calories,
                'protein' : protein,
                'fat': fat,
                'carbs': carbs,
                'ingredients': ingredients,
                'preptime': preptime                
            }

    return Response(json.dumps({"meal added": meal, "code": 201}), mimetype='application/json')


#UPDATE A MEAL
@app.route('/workouts/<int:meal_ID>', methods = ['PUT'])
def update_meal_info(meal_ID):
    try:
        cur = mysql.connection.cursor()
        meal_ID = request.get_json()['meal_ID']
        meal_name = request.get_json()['meal_name']
        calories = request.get_json()['calories']
        protein = request.get_json()['protein']
        fat = request.get_json()['fat']
        carbs = request.get_json()['carbs']
        ingredients = request.get_json()['ingredients']
        preptime = request.get_json()['preptime']


        cur.execute("UPDATE BiteBody.Meals SET meal_name = '"+str(meal_name) + "',calories = '" + str(calories)+ "',protein = '"+ 
        str(protein)+"',fat = '"+ str(fat) + "',carbs = '" + str(carbs)+"',ingredients = '" + str(ingredients)+"',preptime = '" + str(preptime)+
        "'WHERE meal_ID = "+ str(meal_ID)+";")
        mysql.connection.commit()

        meal = { 
                'meal_ID' : meal_ID,
                'meal_name': meal_name,
                'calories': calories,
                'protein' : protein,
                'fat': fat,
                'carbs': carbs,
                'ingredients': ingredients,
                'preptime': preptime                
            }


        return Response(json.dumps({"updated": meal, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yes"}


#DELETE Meal
@app.route('/meals/<int:meal_ID>', methods=['DELETE'])
def delete_meal(meal_ID):
    try:
        cur = mysql.connection.cursor()


        cur.execute("DELETE FROM BiteBody.Meals WHERE meal_ID = " + str(meal_ID) + ";")
        mysql.connection.commit()

        deleted = {
            'id' : meal_ID
        }

        return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"error": "yes"}


#---------------------MEALS-ENDPOINTS-END---------------------#


#---------------------USER LOGIN/REGISTER-ENDPOINTS-START---------------------#


@app.route('/users/register', methods=['POST'])
def register():
    cur = mysql.connection.cursor()

    print(request.get_json())

    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = request.get_json()['password']

    cur.execute("INSERT INTO BiteBody.Users (first_name, last_name, email, password) VALUES ('" 
        + first_name + "', '" 
        + last_name + "', '" 
        + email + "', '" 
        + password + "');")

    mysql.connection.commit()

    posted = {
		'first_name' : first_name,
		'last_name' : last_name,
		'email' : email,
		'password' : password
	}

    return Response(json.dumps({"posted": posted, "code": 201}), mimetype='application/json')


#---------------------USER LOGIN/REGISTER-ENDPOINTS-END---------------------#

#---------------------Calorie calc -ENDPOINTS-START---------------------#

#-----------currently not accurate and needs revisions-------------#

@app.route('/calorie', methods=['POST'])
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
        print(e)
        return {"error": "yes"}

    #---------------------Calorie calc -ENDPOINTS-END---------------------#