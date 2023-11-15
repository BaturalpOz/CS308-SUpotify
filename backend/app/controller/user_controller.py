from flask import Blueprint, request, jsonify, make_response
from werkzeug.exceptions import NotFound, BadRequest
import jwt
import datetime
import os 
from dotenv import load_dotenv
from functools import wraps
from app.services.user_service import UserService

# Load environment variables
load_dotenv()
SECRET_KEY_JWT = os.getenv('SECRET_KEY_JWT')

# Blueprint setup
user_blueprint = Blueprint('user', __name__)
user_service = UserService()

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            raise BadRequest('Token is missing!')

        try:
            data = jwt.decode(token, SECRET_KEY_JWT, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise BadRequest('Token has expired.')
        except jwt.InvalidTokenError:
            raise BadRequest('Token is invalid.')

        return f(*args, **kwargs)
    return decorated

@user_blueprint.route('/signup', methods=['POST'])
def signup_user():
    data = request.get_json()
    if not data or not all(k in data for k in ('username', 'email', 'password')):
        raise BadRequest('Missing username, email, or password.')

    user_id = user_service.create_user(data['username'], data['email'], data['password'])
    if not user_id:
        raise NotFound('Could not create user.')

    return jsonify({'message': 'New user created!', 'user_id': user_id}), 201

@user_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data or not all(k in data for k in ('username_or_email', 'password')):
        raise BadRequest('Missing username/email or password.')

    user = user_service.authenticate_user(data['username_or_email'], data['password'])
    if user is None:
        return jsonify({'message': 'Invalid username/email or password.'}), 401  

    token = jwt.encode({
        'user_id': user.user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY_JWT, algorithm='HS256')

    response = make_response(jsonify({'token': token, 'message': 'User logged in!'}), 200)
    response.set_cookie('access_token_cookie', token, httponly=True, samesite='Strict')
    return response

@user_blueprint.route('/logout', methods=['POST'])
def logout_user():
    response = make_response(jsonify({'message': 'User logged out!'}), 200)
    response.delete_cookie('access_token_cookie')
    return response

@user_blueprint.route('/<user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise NotFound('User not found.')
    return jsonify({'user': user.to_dict()}), 200

@user_blueprint.route('/<user_id>', methods=['PUT'])
@token_required 
def update_user(user_id):
    data = request.get_json()
    if not data:
        raise BadRequest('No data provided for update.')
    user_service.update_user(user_id, data)
    return jsonify({'message': 'User updated!'}), 200

@user_blueprint.route('/<user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    user_service.delete_user(user_id)
    return jsonify({'message': 'User deleted!'}), 200

@user_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify(error=str(e.description)), 400

@user_blueprint.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify(error=str(e.description)), 404
