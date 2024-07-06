from flask import Blueprint, app, request, jsonify
from flask_jwt_extended import create_access_token
from .models import User
from . import db
import bcrypt
import logging

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Creates a new user account.

    Expects a JSON request body containing username and password fields.
    Hashes the password before storing the user in the database.

    Returns:
        JSON response with a message and status code:
            - 201 Created if the user is successfully created.
            - 400 Bad Request if the request is invalid (e.g., missing fields).
            - 500 Internal Server Error if an unexpected error occurs.

    Raises:
        KeyError: If either username or password is missing from the request body.
    """

    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
    except KeyError as e:
        logging.error(f"Missing field in signup request: {e}")
        return jsonify(message="Missing required fields"), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, password=hashed)

    try:
        if User.query.filter_by(username=username).first():
            return jsonify(message="User already exists"), 400
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        return jsonify(message="Failed to create user"), 500

    return jsonify(message="User created"), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Logs in a user and returns an access token on successful authentication.

    Expects a JSON request body containing username and password fields.
    Verifies credentials against the database.

    Returns:
        JSON response with an access token and status code:
            - 200 OK if the login is successful.
            - 401 Unauthorized if the credentials are invalid.
            - 400 Bad Request if the request is invalid (e.g., missing fields).

    Raises:
        KeyError: If either username or password is missing from the request body.
    """

    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
    except KeyError as e:
        logging.error(f"Missing field in login request: {e}")
        return jsonify(message="Missing required fields"), 400

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        logging.error("Invalid login credentials")
        return jsonify(message="Invalid credentials"), 401
