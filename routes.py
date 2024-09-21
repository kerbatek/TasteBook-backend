# routes.py
from flask import Blueprint, jsonify, request
from bson import ObjectId
from datetime import datetime, timedelta
from utils.constants import ERROR_MESSAGES

# ERROR_MESSAGES could then be used in both login and registration routes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
import json
import utils.db_helper as db_helper
import re
import jwt
# Create a Blueprint for user-related routes
users = Blueprint('users', __name__)

from app import jwt as jwtManager
from app import bcrypt
from app import jwt_secret_key

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO format string
        return super(JSONEncoder, self).default(obj)
    

def handle_error(message, status_code=400):
    return jsonify({'message': message}), status_code


def trim_data(data):
    return {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}

# Define the /users route
@users.route('/users', methods=['GET'])
def get_users():
    if request.args.get('user'):
        users = db_helper.select_from_db('users', conditions={'username': request.args.get('user')}, exclude=['password_hash', 'email'], one=True)
    else:
        users = db_helper.select_from_db('users', exclude=['password_hash', 'email'], one=False)
    return json.dumps(users, cls=JSONEncoder, indent=4),200



@users.route('/recipes', methods=['GET'])
def get_recipes():
    if request.args.get('id'):
        try:
            recipes = db_helper.select_from_db('recipes', {'_id': ObjectId(request.args.get('id'))}, one=True)
        except Exception as e:
            return str(e)
    else:
        recipes = db_helper.select_from_db('recipes', one=False)
    return json.dumps(recipes, cls=JSONEncoder, indent=4),200

@users.route('/comment', methods=['POST'])
@jwt_required()
def add_comment():
    comment = request.get_json().get('comment', None)
    recipe_id = request.get_json().get('table_id', None)

    if not all([comment, recipe_id]):
        return handle_error(ERROR_MESSAGES['missing_data'])

    token = request.headers.get('Authorization').removeprefix('Bearer ')
    try:
        decoded_token = jwt.decode(token, jwt_secret_key, algorithms=["HS256"])
    except Exception as e:
        print(e)
        return handle_error(ERROR_MESSAGES['invalid_token'], 401)
    user_id = get_jwt_identity()
    username = get_jwt().get('username')
    date_posted = datetime.now()

    #print(recipe_id, user_id, username, comment, date_posted)
    db_helper.update_db('recipes', {'_id': ObjectId(recipe_id)}, {'$push': {'comments': {'user_id': user_id, 'username': username, 'comment': comment, 'date_posted': date_posted}}})

        
    return jsonify(user_id=user_id, username=username, comment=comment, date_posted=date_posted), 200

@users.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()
    
    if not data:
        return handle_error(ERROR_MESSAGES['missing_data'])
    
    data = trim_data(data)

    if not data.get('email') or not data.get('password'):
        return handle_error(ERROR_MESSAGES['missing_data'])
    data['email'] = data['email'].lower()
    user = db_helper.select_from_db('users', conditions={'email': data['email']}, one=True)
    
    if user:
        password_check = bcrypt.check_password_hash(user['password_hash'], data['password'])
    else:
        password_check = bcrypt.check_password_hash(bcrypt.generate_password_hash('dummy_password').decode('utf-8'), data['password'])

    if not user or not password_check:
        return handle_error(ERROR_MESSAGES['invalid_credentials'], 401)

    # Create access token
    access_token = create_access_token(
    identity=str(user['_id']),  
    additional_claims={
        "username": user['username'],  
    },
    expires_delta=timedelta(hours=24)  
)
    
    return jsonify({'access_token': access_token}), 200

@users.route('/register', methods=['POST'])
def register():
    
    data = request.get_json()
    data = trim_data(data)


    PASSWORD_REGEX = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&#]{8,}$'
    EMAIL_REGEX = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

        # Check if the data object is valid
    if not data:
        return handle_error(ERROR_MESSAGES['missing_data'])

        # Check if fields are empty after trimming
    if not all([data.get('username'), data.get('email'), data.get('password')]):
        return handle_error(ERROR_MESSAGES['missing_data'])


        # Validate username length
    if len(data.get('username', '')) < 3:
        return handle_error(ERROR_MESSAGES['invalid_username'])

        # Validate password with regex (At least 8 characters, 1 letter, 1 number)
    if not re.match(PASSWORD_REGEX, data.get('password', '')):
        return handle_error(ERROR_MESSAGES['invalid_password'])


        # Validate email format with regex
    if not re.match(EMAIL_REGEX, data.get('email', '')):
        return handle_error(ERROR_MESSAGES['invalid_email'])


    if db_helper.select_from_db('users', conditions={'$or':[{'username': data['username']}, {'email': data['email']}]}, one=True):
        return handle_error(ERROR_MESSAGES['user_exists'])


    # Save user to database 
    db_data = {
        'username': data['username'].lower(),
        'email': data['email'].lower(),
        'password_hash': bcrypt.generate_password_hash(data['password']).decode('utf-8'),
        'bio': '',
        'profile_picture_url': '/static/images/default.webp',
        'recipes_uploaded': [],
        'favorites': [],
        'followers': [],
        'following': [],
        'date_joined': datetime.now(),
        'last_login': datetime.now(),
        'display_name': data['username'],
    }
    
    db_helper.insert_to_db('users', db_data)

    return jsonify({'message': 'User registered successfully'}), 201