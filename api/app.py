from flask import Flask, Response, jsonify
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'ODK1LCc5DZ'
app.config['MYSQL_PASSWORD'] = 'pN8S7PFHib'
app.config['MYSQL_DB'] = 'ODK1LCc5DZ'

mysql = MySQL(app)

@app.route('/')
def hello_world():
    return 'Hello, welcome to api.bitebody.xyz! \nThe following below are our endpoints...'

    
@app.route('/users/all', methods=['GET'])
def get_all_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ODK1LCc5DZ.Users;")

    # https://stackoverflow.com/questions/29020839/mysql-fetchall-how-to-get-data-inside-a-dict-rather-than-inside-a-tuple
    # These two lines zips the resulting values with cursor.description
    # otherwise... you would have to do this manually like this:
    # rows = cursor.fetchall()
    # for row in rows:
    #   id = row['id']
    #   col1 = row['col1']
    #   and so on...
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]

    return Response(json.dumps({"users": rows}), mimetype='application/json')
