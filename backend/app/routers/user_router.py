from flask import Blueprint, request, jsonify, make_response
import jwt
import datetime
import os 
from dotenv import load_dotenv
from functools import wraps
from app.services.user_service import UserService

load_dotenv()
SECRET_KEY_JWT = os.getenv('SECRET_KEY_JWT')

user_blueprint = Blueprint('user', __name__)
user_service = UserService()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY_JWT, algorithms=["HS256"])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        current_user = user_service.get_user_by_id(current_user_id)
        if current_user is None:
            return jsonify({'message': 'User not found.'}), 404

        return f(current_user, *args, **kwargs)

    return decorated

@user_blueprint.route('/signup', methods=['POST'])
def signup_user():
    data = request.get_json()

    try:
        user_id = user_service.create_user(data['username'], data['email'], data['password'])
        return jsonify({'message': 'New user created!', 'user_id': user_id}), 201
    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400
    except Exception as e:
        return jsonify({'message': 'Could not create user.', 'error': str(e)}), 500

@user_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    try:
        user = user_service.authenticate_user(data['username'], data['password'])
        token = jwt.encode({
            'user_id': user.user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY_JWT, algorithm='HS256')
        return jsonify({'token': token}), 200
    except ValueError:
        return jsonify({'message': 'Invalid username or password.'}), 401
    except Exception as e:
        return jsonify({'message': 'Login failed.', 'error': str(e)}), 500

@user_blueprint.route('/user', methods=['GET'])
@token_required
def get_user(current_user):
    # 'current_user' parameter is a User object
    user_data = current_user.to_dict()
    return jsonify({'user': user_data}), 200

@user_blueprint.route('/user', methods=['PUT'])
@token_required
def update_user(current_user):
    data = request.get_json()

    try:
        user_service.update_user(current_user.user_id, data)
        return jsonify({'message': 'User updated!'}), 200
    except Exception as e:
        return jsonify({'message': 'Could not update user.', 'error': str(e)}), 500
    
@user_blueprint.route('/user', methods=['DELETE'])
@token_required
def delete_user(current_user):
    try:
        user_service.delete_user(current_user.user_id)
        return jsonify({'message': 'User deleted!'}), 200
    except Exception as e:
        return jsonify({'message': 'Could not delete user.', 'error': str(e)}), 500
