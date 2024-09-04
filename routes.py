# routes.py
from flask import Blueprint, jsonify

# Create a Blueprint for user-related routes
users = Blueprint('users', __name__)

# Define the /users route
@users.route('/users', methods=['GET'])
def get_users():
    # Sample user data
    sample_users = [
        {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com"
        },
        {
            "id": 2,
            "username": "jane_smith",
            "email": "jane@example.com"
        }
    ]
    
    # Return JSON response with the sample users
    return jsonify(sample_users), 200
