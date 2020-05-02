from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os

mysql = MySQL()
bcrypt = Bcrypt()
jwt = JWTManager()

from api.home import home
from api.user import user
from api.collab import collab
from api.workout import workout
from api.youtube_video import youtube_video
from api.meal import meal
from api.calorie_calc import calorie_calc


if __name__ == '__main__':
    app = Flask(__name__)

    app.config['MYSQL_HOST'] = os.getenv('AWS_DB_HOST')
    app.config['MYSQL_USER'] = os.getenv('AWS_DB_USERNAME')
    app.config['MYSQL_PASSWORD'] = os.getenv('AWS_DB_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('AWS_DB_DEFAULT')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    mysql.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)
    

    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(user, url_prefix="/users")
    app.register_blueprint(collab, url_prefix="/collabs")
    app.register_blueprint(workout, url_prefix="/workouts")
    app.register_blueprint(youtube_video, url_prefix="/youtube_videos")
    app.register_blueprint(meal, url_prefix="/meals")
    app.register_blueprint(calorie_calc, url_prefix="/calories")
    app.register_blueprint(calorie_calc, url_prefix="/curated_workouts")

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)