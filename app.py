# app.py
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config import Config
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
jwt_secret_key = app.config['JWT_SECRET_KEY']

# Enable CORS
CORS(app)  # This will allow all origins by default

# Import routes after app initialization
from routes import users

# Register Blueprint
app.register_blueprint(users)

if __name__ == '__main__':
    app.run(debug=True)
