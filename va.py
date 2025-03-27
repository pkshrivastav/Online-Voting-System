from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import json
from functools import wraps
import os

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'your_secret_key'
DATA_FILE = 'data.json'  # File to store user data

# Load data from JSON file
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": []}  # If file doesn't exist, return an empty list
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# JWT Token Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            users = load_data()["users"]
            current_user = next((user for user in users if user["aadhaar_id"] == data["aadhaar_id"] and user["voter_id"] == data["voter_id"]), None)
            if not current_user:
                return jsonify({'message': 'User not found!'}), 403
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    users = load_data()["users"]

    if any(user["aadhaar_id"] == data["aadhaar_id"] or user["voter_id"] == data["voter_id"] for user in users):
        return jsonify({'message': 'User already exists!'}), 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = {
        "name": data["name"],
        "aadhaar_id": data["aadhaar_id"],
        "voter_id": data["voter_id"],
        "password": hashed_password,
        "state": data["state"],
        "sex": data["sex"],
        "age": data["age"],
        "candidate": None,  # Initialize candidate as None
        "has_voted": False
    }
    users.append(new_user)
    save_data({"users": users})

    return jsonify({'message': 'User registered successfully!'})

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    users = load_data()["users"]

    user = next((user for user in users if user["aadhaar_id"] == data["aadhaar_id"] and user["voter_id"] == data["voter_id"]), None)
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({'message': 'Invalid credentials!'}), 401

    token = jwt.encode({'aadhaar_id': user["aadhaar_id"], 'voter_id': user["voter_id"], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
    return jsonify({'token': token})

# Voting Route
@app.route('/vote', methods=['POST'])
@token_required
def vote(current_user):
    data = request.get_json()
    users = load_data()["users"]

    for user in users:
        if user["aadhaar_id"] == current_user["aadhaar_id"] and user["voter_id"] == current_user["voter_id"]:
            if user["has_voted"]:
                return jsonify({'message': 'User has already voted!'}), 400
            
            # Store candidate name
            user["candidate"] = data["candidate"]
            user["has_voted"] = True
            save_data({"users": users})
            return jsonify({'message': f'Vote for {data["candidate"]} submitted successfully!'})

    return jsonify({'message': 'User not found!'}), 404

if __name__ == '__main__':
    if not os.path.exists(DATA_FILE):
        save_data({"users": []})  # Create empty data file if not exists
    app.run(debug=True)
