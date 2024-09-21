# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your_default_jwt_secret_key')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://ubuntupc:27017/tastebook')
