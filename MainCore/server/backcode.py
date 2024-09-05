from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
CORS(app)

# Connect to the MongoDB Atlas cluster
client = MongoClient("mongodb+srv://petwhiz8:VNs3DXlFys93zAzE@cluster1.tdxh1k7.mongodb.net/?retryWrites=true&w=majority")
db = client["clientdatas"]
collection = db["userinfo"]

# Route to handle user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    print("request:", data)  # Get JSON data from the request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Incomplete data provided'}), 400

    # Check if username or email already exists in the database
    existing_user = collection.find_one({'$or': [{'username': username}, {'email': email}]})
    if existing_user:
        return jsonify({'error': 'Username or email is already taken'}), 400

    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(password)

    # Insert new user into the database
    new_user = {
        'username': username,
        'email': email,
        'password': hashed_password
    }
    collection.insert_one(new_user)

    # Return success message
    return jsonify({'message': 'User registered successfully'}), 201

# Route to handle user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json  # Get JSON data from the request
    username = data.get('username')
    password = data.get('password')

    # Find user by username
    user = collection.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        # Return success message or any user-related data
        return jsonify({'success': True, 'message': 'Login successful'}), 200
    else:
        # Return error message for invalid credentials
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401



if __name__ == '__main__':
    app.run(debug=True, port=5008)
