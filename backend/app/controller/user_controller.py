from flask import Blueprint, request, jsonify, make_response
from werkzeug.exceptions import NotFound, BadRequest
import jwt
import datetime
import os
from dotenv import load_dotenv
from functools import wraps
import json

from app.services.user_service import UserService
from app.services.recommendation_service import RecommendationService


# Load environment variables
load_dotenv()
SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")

# Blueprint setup
user_blueprint = Blueprint("user", __name__)
user_service = UserService()
recommendation_service = RecommendationService()


# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Cookie")
        if not token:
            raise BadRequest("Token is missing!")
        try:
            token = token.split("=")[1]
            data = jwt.decode(token, SECRET_KEY_JWT, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise BadRequest("Token has expired.")
        except jwt.InvalidTokenError:
            raise BadRequest("Token is invalid.")
        except:
            raise BadRequest("Token is missing!:()")

        user_id = data.get("user_id")
        if not user_id:
            raise BadRequest("User ID is missing in token.")

        return f(*args, **kwargs, user_id=user_id)

    return decorated


@user_blueprint.route("/signup", methods=["POST"])
def signup_user():
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "email", "password")):
        raise BadRequest("Missing username, email, or password.")

    user_id = user_service.create_user(
        data["username"], data["email"], data["password"]
    )
    if not user_id:
        raise NotFound("Could not create user.")

    return jsonify({"message": "New user created!", "user_id": user_id}), 201


@user_blueprint.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    if not data or not all(k in data for k in ("username_or_email", "password")):
        raise BadRequest("Missing username/email or password.")

    user = user_service.authenticate_user(data["username_or_email"], data["password"])
    if user is None:
        return jsonify({"message": "Invalid username/email or password."}), 401
    token = jwt.encode(
        {
            "user_id": user.user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        },
        SECRET_KEY_JWT,
        algorithm="HS256",
    )

    response = make_response(
        jsonify({"token": token, "message": "User logged in!"}), 200
    )
    response.set_cookie("access_token_cookie", token, httponly=True, samesite="Strict")
    return response


@user_blueprint.route("/logout", methods=["POST"])
def logout_user():
    response = make_response(jsonify({"message": "User logged out!"}), 200)
    response.delete_cookie("access_token_cookie")
    return response


@user_blueprint.route("/<userid>", methods=["GET"])
@token_required
def get_user(user_id, userid):
    user = user_service.get_user_by_id(userid)
    if user is None:
        raise NotFound("User not found.")
    return jsonify({"user": user.to_dict()}), 200


@user_blueprint.route("/<userid>", methods=["PUT"])
@token_required
def update_user(user_id, userid):
    data = request.get_json()
    if not data:
        raise BadRequest("No data provided for update.")
    user_service.update_user(userid, data)
    return jsonify({"message": "User updated!"}), 200


@user_blueprint.route("/<userid>", methods=["DELETE"])
@token_required
def delete_user(user_id, userid):
    user_service.delete_user(userid)
    return jsonify({"message": "User deleted!"}), 200


@user_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify(error=str(e.description)), 400


@user_blueprint.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify(error=str(e.description)), 404


"""
      <form action = "http://localhost:5000/user/upload" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "a.json" />
"""


@user_blueprint.route("/upload", methods=["POST"])
@token_required
def file_upload(user_id):
    file = request.files["file"]
    if not file:
        raise BadRequest("No file provided.")
    if file.mimetype != "application/json":
        raise BadRequest("File must be a JSON file.")
    if request.content_length > 1000000:
        raise BadRequest("File too large.")

    file_data = file.read()

    file_data = file_data.decode("utf-8")

    file_data = json.loads(file_data)

    return (
        jsonify(
            {"message": "File uploaded!", "uploaded": file_data, "uploader": user_id}
        ),
        200,
    )


@user_blueprint.route("/add-friend", methods=["POST"])
@token_required
def add_friend(user_id):
    data = request.get_json()
    if not data or not "friend_username" in data:
        raise BadRequest("Missing username")
    friends = user_service.add_friend(user_id, data["friend_username"])
    if not friends:
        raise BadRequest("Could not add friend.")
    return jsonify({"message": "Friend added!", "friends": friends}), 200


@user_blueprint.route("/remove-friend", methods=["POST"])
@token_required
def remove_friend(user_id):
    data = request.get_json()
    if not data or not "friend_username" in data:
        raise BadRequest("Missing username")
    friends = user_service.remove_friend(user_id, data["friend_username"])
    return jsonify({"message": "Friend removed!", "friends": friends}), 200


@user_blueprint.route("/friends", methods=["GET"])
@token_required
def get_friends(user_id):
    friends = user_service.get_friends(user_id)
    return jsonify({"message": "Friends retrieved!", "friends": friends}), 200


@user_blueprint.route("/recommendations", methods=["GET"])
@token_required
def get_recommendations(user_id):
    try:
        recommendations = recommendation_service.generate_recommendations(user_id)
        return (
            jsonify(
                {
                    "message": "Recommendations fetched successfully",
                    "recommendations": recommendations,
                }
            ),
            200,
        )
    except Exception as e:
        raise BadRequest(str(e))
