# auth.py
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from datetime import datetime
from bson.objectid import ObjectId
import os
# Create a blueprint for authentication
auth = Blueprint('auth', __name__)

MONGO_URI = os.getenv('MONGO_URI')

# MongoDB setup (this could be imported from a shared module or config)
client = MongoClient(MONGO_URI)  # Replace with your MONGO_URI
db = client['Encrypto']  # Database name
users = db['users']  # Collection for storing users

bcrypt = Bcrypt()  # We will initialize bcrypt later

# Signup route (expects JSON data with username, email, and password)
@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing username, email or password'}), 400

    # Hash the password before storing
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Check if user already exists
    existing_user = users.find_one({'email': email})

    if existing_user:
        return jsonify({'error': 'User with this email already exists!'}), 409

    # Create new user with createdAt timestamp
    new_user = {
        'username': username,
        'email': email,
        'password': hashed_password,
        'createdAt': datetime.utcnow()  # Store UTC timestamp for user creation
    }
    result = users.insert_one(new_user)  # Insert the new user

    # Return the ObjectId, username, and email in the response
    return jsonify({
        'message': 'User created successfully!',
        'user': {
            'id': str(result.inserted_id),  # Convert ObjectId to string
            'username': username,
            'email': email
        }
    }), 201

# Login route (expects JSON data with email and password)
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    # Find the user by email
    user = users.find_one({'email': email})

    if user and bcrypt.check_password_hash(user['password'], password):
        # Return ObjectId, username, and email upon successful login
        return jsonify({
            'message': 'Login successful!',
            'user': {
                'id': str(user['_id']),  # Convert ObjectId to string
                'username': user['username'],
                'email': user['email']
            }
        }), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401
