from flask import Flask, Response
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, welcome to api.bitebody.xyz! \nThe following below are our endpoints...'

    
@app.route('/users/all', methods=['GET'])
def get_all_users():
    users = [
        {"name": "Bryan Rojas", "email": "bryanrojascs@gmail.com"},
        {"name": "David Ibarra", "email": "davidibarra@gmail.com"}
    ]

    return Response(json.dumps({"users": users}), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)