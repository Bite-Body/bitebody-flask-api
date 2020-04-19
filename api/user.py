from flask import Blueprint, Response, json, request
from flask_mysqldb import MySQL
from logger import post_log
from flask_jwt_extended import (create_access_token)
#import api.email_Test 
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


import string
import random

user = Blueprint("user", __name__)

from manage import mysql as mysql
from manage import bcrypt as bcrypt
from manage import jwt as jwt

@user.route('/all', methods=['GET'])
def get_all_users():
    try:
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
            temp_user['username'] = row[5]
            all_users.append(temp_user)

        post_log('GET /users/all')

        return Response(json.dumps({"users": all_users, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrive all users.", "error message": str(e)}

@user.route('/<int:userID>', methods=['GET'])
def find_user(userID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BiteBody.Users WHERE id = "+str(userID)+";")
        row = cur.fetchone()
        user = {
            'first_name':row[1],
            'last_name':row[2],
            'email' : row[3],
            'username' : row[5],
            'id' : row[0]
        }

        post_log('GET /users/<int:userID>')
        return Response(json.dumps({"user": user, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to retrieve this user.", "error message": str(e)}
        
@user.route('/<int:userID>', methods=['DELETE'])
def delete_user(userID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM BiteBody.Users Where id = " +str(userID) +  ";")
        row = cur.fetchone()
        foundID = row[0]
        if foundID == None:
            return {"NOT FOUND":"User want to delete doesn't exist"}
        else:
            cur.execute("DELETE FROM BiteBody.Users WHERE id = " + str(userID) + ";")
            mysql.connection.commit()
            deleted = {
                'id' : userID
            }

            post_log('DELETE /users/<int:userID>')
            return Response(json.dumps({"deleted": deleted, "code": 200}), mimetype='application/json')
    except Exception as e:
        return {"Error": "Unable to delete this user.", "error message": str(e)}

@user.route('/<int:userID>', methods = ['PUT'])
def update_user_info(userID):
    try:
        cur = mysql.connection.cursor()
        first_name = request.get_json()['first_name']
        last_name = request.get_json()['last_name']
        email = request.get_json()['email']
        password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
        username = request.get_json()['username']
        cur.execute("UPDATE BiteBody.Users SET first_name = '"+str(first_name) + "',last_name = '" + str(last_name)+ "',email = '"+ str(email)+ "',password = '"+ str(password) + "',username = '"+ str(username) + 
        "'WHERE id = "+ str(userID)+";")
        mysql.connection.commit()
        updated = {
            'first_name':first_name,
            'last_name':last_name,
            'email' : email,
            'password' : password,
            'username' : username
        }
        

        post_log('PUT /users/<int:userID>')
        return Response(json.dumps({"updated": updated, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"Error": "Unable to update this user.", "error message": str(e)}

@user.route('', methods=['POST'])
def create_user():
    try:
        cur = mysql.connection.cursor()
        first_name = request.get_json()['first_name']
        last_name = request.get_json()['last_name']
        email = request.get_json()['email']
        username = request.get_json()['username']
        
        cur.execute("SELECT email FROM BiteBody.Users WHERE email = %(email)s", {'email': email})
        emailFound = cur.fetchone()

        cur.execute("SELECT email FROM BiteBody.Users WHERE username = %(username)s", {'username': username})
        usernameFound = cur.fetchone()


        if '@' not in email:
            return {"Error": "Not a valid email"}

        if(emailFound or usernameFound):
            post_log('POST /users FAILED')
            return {"Error": "Can't add already existing email or username"}
        else:
            password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')

            cur.execute("INSERT INTO BiteBody.Accounts_In_Limbo (first_name, last_name, email, password, username) VALUES ('" 
                + first_name + "', '" 
                + last_name + "', '" 
                + email + "', '" 
                + password + "', '" 
                + username + "');")
            mysql.connection.commit()

            port = 465  # For SSL
            smtp_server = "smtp.gmail.com"
            sender = "bitebodyxyztest@gmail.com"
            Email_Password = "tester_account404"
            conf_key = randomPassword()

            ##START
            cur.execute("UPDATE BiteBody.Accounts_In_Limbo SET confirmation_key = '"+conf_key+ "' WHERE email = %(email)s", {'email': email})

            mysql.connection.commit() #necessary for data modification
            message = MIMEMultipart("alternative")
            message["subject"] = "Account Recovery For Bitebody.xyz"
            message["From"] = sender
            message["To"] = email


            html = """\
            <html>
                <body>
                <p>Thank you for signing up for a BITEBODY account! <br>
                    <a href="https://www.google.com">CLICK RIGHT HERE</a> 
                    to complete your account registration!

                    Your registration code is: <b>{conf_key}</b> 
                    Make sure to enter it when prompted.
                </p>
                </body>
            </html>
            """.format(conf_key = conf_key)

            # Turn these into plain/html MIMEText objects
            #part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            #message.attach(part1)
            message.attach(part2)


            # Create a secure SSL context
            context = ssl.create_default_context()


            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender, Email_Password)
                server.sendmail(sender,email,message.as_string())
                # TODO: Send email here
            ##END



            
            cur.execute("INSERT INTO BiteBody.Users (first_name, last_name, email, password, username) VALUES ('" 
                + first_name + "', '" 
                + last_name + "', '" 
                + email + "', '" 
                + password + "', '" 
                + username + "');")
            mysql.connection.commit()
            
            posted = {
                'first_name' : first_name, 
                'last_name' : last_name,
                'email' : email,
                'password' : password,
                'username' : username
            }

            post_log('POST /users')
            return Response(json.dumps({"posted": posted, "code": 201}), mimetype='application/json')
    except Exception as e:
        print(e)
        return {"Error": "Unable to create this user.", "ErrorMessage": str(e)}

@user.route('finalize-registration', methods=['POST'])
def finalize_user():
    try:
        cur = mysql.connection.cursor()
        reg_key = request.get_json()['regKey']
        cur.execute ("SELECT * FROM BiteBody.Accounts_In_Limbo WHERE confirmation_key = %(confirmation_key)s", {'confirmation_key': reg_key})
        #if(cur.fetchone)
        #{
        cur.execute("INSERT INTO BiteBody.Users (first_name, last_name, email, password, username) SELECT first_name, last_name, email, password, username FROM BiteBody.Accounts_In_Limbo WHERE confirmation_key = %(confirmation_key)s", {'confirmation_key':reg_key})

        cur.execute("DELETE FROM BiteBody.Accounts_In_Limbo WHERE confirmation_key = %(confirmation_key)s", {'confirmation_key': reg_key})
        #}
        #If above returns something (NOT NULL):
            #copy that entire content of that row into the USERS table
            #erase the entry querried in line 222 from imbo table
        #else:
            #print warning saying that they need to type in correct registration key
    except Exception as e:
        print(e)
        return {
            "Error": "Incorrect email or password.",
            "Allow": "no"
        }

@user.route('/login', methods=['POST'])
def login():
    try:
        cur = mysql.connection.cursor()
        username_or_email = request.get_json()['username_or_email']
        password = request.get_json()['password']
        
        cur.execute("SELECT * FROM BiteBody.Users where username = %(username)s", {'username': username_or_email})
        rv = cur.fetchone()

        cur.execute("SELECT * FROM BiteBody.Users where email = %(email)s", {'email': username_or_email})
        rv_email = cur.fetchone()

        result = ''

        try:
            if bcrypt.check_password_hash(rv[4], password):
                access_token = create_access_token(identity = {'first_name': rv[1],'last_name': rv[2],'email': rv[3],'id': rv[0], 'username': rv[5]})
                result = access_token
            else:
                raise Exception('Passwords do not match')
        except:
            try:
                if bcrypt.check_password_hash(rv_email[4], password):
                    access_token = create_access_token(identity = {'first_name': rv_email[1],'last_name': rv_email[2],'email': rv_email[3],'id': rv_email[0], 'username': rv_email[5]})
                    result = access_token
                else:
                    raise Exception('Passwords do not match')
            except:
                raise Exception('Passwords do not match')
        
        custom_msg = 'POST /users/login for ' + username_or_email
        post_log(custom_msg)

        return result
    except Exception as e:
        print(e)
        return {
            "Error": "Incorrect email or password.",
            "Allow": "no"
        }

@user.route('/forgot-password', methods = ['POST'])
def forgot_password():
    try:
        cur = mysql.connection.cursor()
        email = request.get_json()['email']

        if '@' not in email:
            return {"Error": "Not a valid email"}

        cur.execute("SELECT * FROM BiteBody.Users where email = %(email)s", {'email': email})
        email_exists = cur.fetchone()
        if(email_exists):
            port = 465  # For SSL
            smtp_server = "smtp.gmail.com"
            sender = "bitebodyxyztest@gmail.com"
            #getter = "bitebodyxyz@gmail.com"

            password = "tester_account404"

            newTempPass = randomPassword()
            cur.execute("UPDATE BiteBody.Users SET password_reset_key = '"+newTempPass+ "' WHERE email = %(email)s", {'email': email})
            # cur.execute("INSERT INTO BiteBody.Users (password_reset_key) VALUES ('" 
            #     + newTempPass +"');")
            mysql.connection.commit() #necessary for data modification
            message = MIMEMultipart("alternative")
            message["subject"] = "Account Recovery For Bitebody.xyz"
            message["From"] = sender
            message["To"] = email
            #trivial

            html = """\
            <html>
                <body>
                <p>You are receiving this email because your recent account activity shows you are in need of a replacement password.<br>
                    <a href="https://www.bitebody.xyz/reset-password">CLICK RIGHT HERE</a> 
                    to reset your account's password.
                    Your Temp Password is: <b>{newTempPass}</b> 
                    Make sure to enter it when prompted.
                </p>
                </body>
            </html>
            """.format(newTempPass = newTempPass)

            # Turn these into plain/html MIMEText objects
            #part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            #message.attach(part1)
            message.attach(part2)


            # Create a secure SSL context
            context = ssl.create_default_context()


            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender, password)
                server.sendmail(sender,email,message.as_string())
                # TODO: Send email here
            
            post_log('POST /users/forgot-password')
            return {"Allow": "yes"}
        else:
            return {"Error": "Email entered is not a member of Bitebody.xyz"}
    except Exception as e:
        print(e)
        return {"Error": "Unable to perform operation.", "Error Message": str(e)}

def randomPassword(stringLength=8):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


@user.route('/reset-password', methods = ['POST'])
def reset_password():
    try:
        cur = mysql.connection.cursor()
        email = request.get_json()['email']

        if '@' not in email:
            return {"Error": "Not a valid email"}

        password = request.get_json()['password']
        confirmed_password = request.get_json()['confirmed_password']
        input_reset_key = request.get_json()['reset_key']
        cur.execute ("SELECT password_reset_key FROM BiteBody.Users WHERE email = %(email)s", {'email': email})
        raw_reset_key_in_DB = str(cur.fetchone())
        mod_reset_key_in_DB = raw_reset_key_in_DB
        chars_to_delete = "(',)"
        for character in chars_to_delete:
            mod_reset_key_in_DB = mod_reset_key_in_DB.replace(character, "")
        encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
        if(mod_reset_key_in_DB == input_reset_key):
            if(password == confirmed_password):
                cur.execute("UPDATE BiteBody.Users SET password_reset_key = NULL;")
                cur.execute("UPDATE BiteBody.Users SET password = '"+encrypted_password+ "' WHERE email = %(email)s", {'email': email})
                #cur.execute("UPDATE BiteBody.Users SET password = '"+password+           "' WHERE (email = '"+str(email)+"');")
                mysql.connection.commit()
                post_log('POST /reset-password')
                return {"Allow": "yes"}
            else:
                return {"Error": "Passwords do not match!", "Allow":"No", "Password": password, "Conf Pass": confirmed_password}
        else:
            return {"Error": str(mod_reset_key_in_DB)+"/"+str(input_reset_key)+"/"+str(encrypted_password)}

    except Exception as e:
        return {
            "Error": str(e),
            "Allow": "no"
        }
