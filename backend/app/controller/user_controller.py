from flask import Blueprint, request, jsonify, make_response, render_template
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


@user_blueprint.route("/rate-song", methods=["POST"])
@token_required
def rate_song(user_id):
    data = request.get_json()
    if not data or not "song" in data or not "rate" in data:
        raise BadRequest("Missing song or rate")
    rated_songs = user_service.rate_song(user_id, data["song"], data["rate"])
    return jsonify({"message": "Song rated!", "rated_songs": rated_songs}), 200


@user_blueprint.route("/unrate-song", methods=["POST"])
@token_required
def unrate_song(user_id):
    data = request.get_json()
    if not data or not "song" in data:
        raise BadRequest("Missing song")
    rated_songs = user_service.unrate_song(user_id, data["song"])
    return jsonify({"message": "Song unrated!", "rated_songs": rated_songs}), 200


@user_blueprint.route("/get-rated-songs", methods=["GET"])
@token_required
def get_rated_songs(user_id):
    rated_songs = user_service.get_rated_songs(user_id)
    return (
        jsonify({"message": "Rated songs retrieved!", "rated_songs": rated_songs}),
        200,
    )


@user_blueprint.route("/rate-album", methods=["POST"])
@token_required
def rate_album(user_id):
    data = request.get_json()
    if not data or not "album" in data or not "rate" in data:
        raise BadRequest("Missing album or rate")
    rated_albums = user_service.rate_album(user_id, data["album"], data["rate"])
    return jsonify({"message": "Album rated!", "rated_albums": rated_albums}), 200


@user_blueprint.route("/unrate-album", methods=["POST"])
@token_required
def unrate_album(user_id):
    data = request.get_json()
    if not data or not "album" in data:
        raise BadRequest("Missing album")
    rated_albums = user_service.unrate_album(user_id, data["album"])
    return jsonify({"message": "Album unrated!", "rated_albums": rated_albums}), 200


@user_blueprint.route("/get-rated-albums", methods=["GET"])
@token_required
def get_rated_albums(user_id):
    rated_albums = user_service.get_rated_albums(user_id)
    return (
        jsonify({"message": "Rated albums retrieved!", "rated_albums": rated_albums}),
        200,
    )


@user_blueprint.route("/rate-artist", methods=["POST"])
@token_required
def rate_artist(user_id):
    data = request.get_json()
    if not data or not "artist" in data or not "rate" in data:
        raise BadRequest("Missing artist or rate")
    rated_artists = user_service.rate_artist(user_id, data["artist"], data["rate"])
    return jsonify({"message": "Artist rated!", "rated_artists": rated_artists}), 200


@user_blueprint.route("/unrate-artist", methods=["POST"])
@token_required
def unrate_artist(user_id):
    data = request.get_json()
    if not data or not "artist" in data:
        raise BadRequest("Missing artist")
    rated_artists = user_service.unrate_artist(user_id, data["artist"])
    return jsonify({"message": "Artist unrated!", "rated_artists": rated_artists}), 200


@user_blueprint.route("/get-rated-artists", methods=["GET"])
@token_required
def get_rated_artists(user_id):
    rated_artists = user_service.get_rated_artists(user_id)
    return (
        jsonify(
            {"message": "Rated artists retrieved!", "rated_artists": rated_artists}
        ),
        200,
    )

@user_blueprint.route("/statistics", methods=["GET"])
@token_required
def get_statistics(user_id):
    # Extract query parameters for date constraints and other filters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    # Convert string dates to datetime objects, handle the case when dates are not provided
    start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
    end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

    # Retrieve data from the database, filtering by the user and the date constraints
    # This could be a complex operation depending on your database schema and the size of the data
    # Let's assume you have a function in your user_service that handles this
    data = user_service.get_user_statistics(user_id, start_date, end_date)

    # Convert the data to a format suitable for rendering in tables or charts
    # For example, you could convert it to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # You can now convert the DataFrame to various formats for tables or to be sent to the frontend for chart rendering
    # For example, to get top 10 albums from the 90s
    top_albums_90s = df[(df['year'] >= 1990) & (df['year'] < 2000)].nlargest(10, 'rating')
    
    # To get favorite 10 songs added in the last 6 months
    six_months_ago = datetime.utcnow() - timedelta(months=6)
    top_songs_last_6_months = df[df['date_added'] >= six_months_ago].nlargest(10, 'rating')
    
    # Convert your DataFrame to JSON or any other format that your frontend can handle
    top_albums_90s_json = top_albums_90s.to_json(orient='records')
    top_songs_last_6_months_json = top_songs_last_6_months.to_json(orient='records')

    # Render the statistics page and pass the data
    return render_template('statistics.html', 
                           top_albums_90s=top_albums_90s_json, 
                           top_songs_last_6_months=top_songs_last_6_months_json)

@user_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify(error=str(e.description)), 400


@user_blueprint.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify(error=str(e.description)), 404
