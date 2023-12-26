from flask import Blueprint, request, jsonify, make_response, render_template
from werkzeug.exceptions import NotFound, BadRequest
import jwt
import datetime
import os
from dotenv import load_dotenv
from functools import wraps
import json

from app.services.user_service import UserService
from app.services.song_service import SongService
from app.services.recommendation_service import RecommendationService


# Load environment variables
load_dotenv()
SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")

# Blueprint setup
user_blueprint = Blueprint("user", __name__)
user_service = UserService()
song_service = SongService()
recommendation_service = RecommendationService()


# Authentication decorator
def token_required(f):
    """Decorator for token required"""

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
        except Exception as exc:
            print(exc)
            raise BadRequest("Token is missing!:()")

        user_id = data.get("user_id")
        if not user_id:
            raise BadRequest("User ID is missing in token.")

        return f(*args, **kwargs, user_id=user_id)

    return decorated


@user_blueprint.route("/signup", methods=["POST"])
def signup_user():
    """
    Signup user
    params:
        username: username of user
        email: email of user
        password: password of user
    return:
        message: message of success
        user_id: id of user
    """
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
    """
    Login user
    params:
        username_or_email: username or email of user
        password: password of user
    return:
        token: token of user
        message: message of success
    """
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
    response.set_cookie(
        "access_token_cookie",
        value=token,
        domain="localhost",
        httponly=True,
        samesite="None",
        secure=False,
        path="/",
    )
    return response


@user_blueprint.route("/logout", methods=["POST"])
def logout_user():
    """
    Logout user
    return:
        message: message of success
    """
    response = make_response(jsonify({"message": "User logged out!"}), 200)
    response.delete_cookie("access_token_cookie")
    return response


@user_blueprint.route("/<userid>", methods=["GET"])
@token_required
def get_user(user_id, userid):
    """
    Get user by id
    params:
        userid: id of user
    return:
        user: user object
    """
    user = user_service.get_user_by_id(userid)
    if user is None:
        raise NotFound("User not found.")
    return jsonify({"user": user.to_dict()}), 200


@user_blueprint.route("/<userid>", methods=["PUT"])
@token_required
def update_user(user_id, userid):
    """
    Update user
    params:
        userid: id of user
    return:
        message: message of success
    """
    data = request.get_json()
    if not data:
        raise BadRequest("No data provided for update.")
    user_service.update_user(userid, data)
    return jsonify({"message": "User updated!"}), 200


@user_blueprint.route("/<userid>", methods=["DELETE"])
@token_required
def delete_user(user_id, userid):
    """
    Delete user
    params:
        userid: id of user
    return:
        message: message of success
    """
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
    """
    Upload file
    params:
        user_id: id of user
    return:
        message: message of success
    """
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


@user_blueprint.route("/profile", methods=["GET"])
@token_required
def get_user_profile(user_id):
    """
    Get user profile
    params:
        user_id: id of user
    return:
        name: name of user
        email: email of user
    """
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise NotFound("User not found.")
    return jsonify({"name": user.username, "email": user.email}), 200


@user_blueprint.route("/add-friend", methods=["POST"])
@token_required
def add_friend(user_id):
    """
    Add friend
    params:
        friend_username: username of friend
    return:
        message: message of success
    """
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
    """
    Remove friend
    params:
        friend_username: username of friend
    return:
        message: message of success
    """
    data = request.get_json()
    if not data or not "friend_username" in data:
        raise BadRequest("Missing username")
    friends = user_service.remove_friend(user_id, data["friend_username"])
    return jsonify({"message": "Friend removed!", "friends": friends}), 200


@user_blueprint.route("/friends", methods=["GET"])
@token_required
def get_friends(user_id):
    """
    Get friends for user
    params:
        user_id: id of user
    return:
        friends: list of friends
    """
    friends = user_service.get_friends(user_id)
    return jsonify({"message": "Friends retrieved!", "friends": friends}), 200


@user_blueprint.route("/recommendations", methods=["GET"])
@token_required
def get_recommendations(user_id):
    """
    Get recommendations for user
    params:
        user_id: id of user
    return:
        recommendations: list of recommendations
    """
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
    """
    Rate song
    params:
        song: name of song
        rate: rating of song
    return:
        message: message of success
    """
    data = request.get_json()
    if not data or not "song" in data or not "rate" in data:
        raise BadRequest("Missing song or rate")
    rated_songs = user_service.rate_song(user_id, data["song"], data["rate"])
    return jsonify({"message": "Song rated!", "rated_songs": rated_songs}), 200


@user_blueprint.route("/unrate-song", methods=["POST"])
@token_required
def unrate_song(user_id):
    """
    Unrate song
    params:
        song: name of song
    return:
        message: message of success
    """
    data = request.get_json()
    if not data or not "song" in data:
        raise BadRequest("Missing song")
    rated_songs = user_service.unrate_song(user_id, data["song"])
    return jsonify({"message": "Song unrated!", "rated_songs": rated_songs}), 200


@user_blueprint.route("/get-rated-songs", methods=["GET"])
@token_required
def get_rated_songs(user_id):
    """
    Get rated songs
    params:
        user_id: id of user
    return:
        rated_songs: list of rated songs
    """
    rated_songs = user_service.get_rated_songs(user_id)
    return (
        jsonify({"message": "Rated songs retrieved!", "rated_songs": rated_songs}),
        200,
    )


@user_blueprint.route("/rate-album", methods=["POST"])
@token_required
def rate_album(user_id):
    """
    Rate album
    params:
        album: name of album
        rate: rating of album
    return:
        message: message of success
    """
    data = request.get_json()
    if not data or not "album" in data or not "rate" in data:
        raise BadRequest("Missing album or rate")
    rated_albums = user_service.rate_album(user_id, data["album"], data["rate"])
    return jsonify({"message": "Album rated!", "rated_albums": rated_albums}), 200


@user_blueprint.route("/unrate-album", methods=["POST"])
@token_required
def unrate_album(user_id):
    """
    Unrate album
    params:
        album: name of album
    return:
        message: message of success
    """
    data = request.get_json()
    if not data or not "album" in data:
        raise BadRequest("Missing album")
    rated_albums = user_service.unrate_album(user_id, data["album"])
    return jsonify({"message": "Album unrated!", "rated_albums": rated_albums}), 200


@user_blueprint.route("/get-rated-albums", methods=["GET"])
@token_required
def get_rated_albums(user_id):
    """
    Get rated albums
    params:
        user_id: id of user
    return:
        rated_albums: list of rated albums
    """
    rated_albums = user_service.get_rated_albums(user_id)
    return (
        jsonify({"message": "Rated albums retrieved!", "rated_albums": rated_albums}),
        200,
    )


@user_blueprint.route("/rate-artist", methods=["POST"])
@token_required
def rate_artist(user_id):
    """
    Rate artist
    params:
        artist: name of artist
        rate: rating of artist
    return:
        message: message of success
    """
    data = request.get_json()
    if not data or not "artist" in data or not "rate" in data:
        raise BadRequest("Missing artist or rate")
    rated_artists = user_service.rate_artist(user_id, data["artist"], data["rate"])
    return jsonify({"message": "Artist rated!", "rated_artists": rated_artists}), 200


@user_blueprint.route("/unrate-artist", methods=["POST"])
@token_required
def unrate_artist(user_id):
    """
    Unrate artist
    params:
        artist: name of artist
    return:
        message: message of success
    """
    data = request.get_json()
    if not data or not "artist" in data:
        raise BadRequest("Missing artist")
    rated_artists = user_service.unrate_artist(user_id, data["artist"])
    return jsonify({"message": "Artist unrated!", "rated_artists": rated_artists}), 200


@user_blueprint.route("/get-rated-artists", methods=["GET"])
@token_required
def get_rated_artists(user_id):
    """
    Get rated artists
    params:
        user_id: id of user
    return:
        rated_artists: list of rated artists
    """
    rated_artists = user_service.get_rated_artists(user_id)
    return (
        jsonify(
            {"message": "Rated artists retrieved!", "rated_artists": rated_artists}
        ),
        200,
    )


@user_blueprint.route("/statistics", methods=["POST"])
@token_required
def get_statistics(user_id):
    """
    Get statistics for user
    params:
        user_id: id of user
        start_date: start date of statistics
        end_date: end date of statistics
        filter_type: type of filter
    return:
        rated_songs: list of rated songs
        rated_albums: list of rated albums
        rated_artists: list of rated artists
    """
    data = request.get_json()
    """
    {
    "start_date": "%Y-%m-%d", 
    "end_date": "%Y-%m-%d",
    "filter_type": "user" | "songs" | "albums" | "artists"
    }"""

    try:
        start_date = data["start_date"]
        end_date = data["end_date"]
        filter_type = data["filter_type"]
    except KeyError:
        raise BadRequest("Missing start_date or end_date or filter_type")
    # Convert string dates to datetime objects, handle the case when dates are not provided
    start_date = (
        datetime.datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    )
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    if filter_type == "songs":
        rated_songs = user_service.get_rated_songs_by_date(
            user_id, start_date, end_date
        )
        return (
            jsonify({"message": "Statistics retrieved!", "rated_songs": rated_songs}),
            200,
        )
    elif filter_type == "albums":
        rated_albums = user_service.get_rated_albums_by_date(
            user_id, start_date, end_date
        )
        return (
            jsonify({"message": "Statistics retrieved!", "rated_songs": rated_albums}),
            200,
        )
    elif filter_type == "artists":
        rated_artists = user_service.get_rated_artists_by_date(
            user_id, start_date, end_date
        )
        return (
            jsonify({"message": "Statistics retrieved!", "rated_songs": rated_artists}),
            200,
        )
    elif filter_type == "user":
        # Frontend should give me last 6 month as a date range, not as a string "6 month".
        user_ratings = user_service.get_user_ratings_by_date(
            user_id, start_date, end_date
        )
        return (
            jsonify({"message": "Statistics retrieved!", "rated_songs": user_ratings}),
            200,
        )
    raise BadRequest("Invalid filter type")


@user_blueprint.route("/statistics-user", methods=["POST"])
@token_required
def get_statistics_user(user_id):
    """
    Get statistics for user
    params:
        user_id: id of user
    return:
        rated_songs: list of rated songs
        rated_albums: list of rated albums
        rated_artists: list of rated artists
    """
    data = request.get_json()
    # all songs and artists and albums rated by user sorted by date
    return (
        jsonify(
            {
                "message": "Statistics retrieved!",
                "rated_songs": user_service.get_ratings_for_user(user_id, "songs"),
                "rated_albums": user_service.get_ratings_for_user(user_id, "albums"),
                "rated_artists": user_service.get_ratings_for_user(user_id, "artists"),
            }
        ),
        200,
    )


@user_blueprint.route("/add-playlist", methods=["POST"])
@token_required
def add_playlist(user_id):
    """
    Add playlist
    params:
        playlist_name: name of playlist
        song_names: list of song names
    return:
        message: message of success
    """
    data = request.get_json()
    if not data or not "playlist_name" in data or not "song_names" in data:
        raise BadRequest("Missing playlist_name or song_names in the request body")
    playlist_name = data["playlist_name"]
    song_names = data["song_names"]
    user_service.add_playlist(user_id, playlist_name, song_names)
    return jsonify({"message": "Playlist added!"}), 201


@user_blueprint.route("/delete-playlist", methods=["DELETE"])
@token_required
def delete_playlist(user_id):
    """
    Delete playlist
    params:
        playlist_name: name of playlist
    return:
        message: message of success
    """
    data = request.get_json()
    if not data or not "playlist_name" in data:
        raise BadRequest("Missing playlist_name in the request body")
    playlist_name = data["playlist_name"]
    user_service.delete_playlist(user_id, playlist_name)
    return jsonify({"message": "Playlist deleted!"}), 200


@user_blueprint.route("/add-song-to-playlist", methods=["POST"])
@token_required
def add_song_to_playlist(user_id):
    """
    Add song to playlist
    params:
        playlist_name: name of playlist
        song_name: name of song
    return:
        message: message of success
    """
    data = request.get_json()
    if not data or not all(key in data for key in ("playlist_name", "song_name")):
        raise BadRequest("Missing playlist_name or song_name in the request body")
    playlist_name = data["playlist_name"]
    song_name = data["song_name"]
    user_service.add_song_to_playlist(user_id, playlist_name, song_name)
    return jsonify({"message": "Song added to playlist!"}), 201


@user_blueprint.route("/delete-song-from-playlist", methods=["DELETE"])
@token_required
def delete_song_from_playlist(user_id):
    """
    Delete song from playlist
    params:
        playlist_name: name of playlist
        song_name: name of song
    return:
        message: message of success
    """
    data = request.get_json()
    if not data or not all(k in data for k in ("playlist_name", "song_name")):
        raise BadRequest("Missing playlist_name or song_name in the request body")
    playlist_name = data["playlist_name"]
    song_name = data["song_name"]
    user_service.delete_song_from_playlist(user_id, playlist_name, song_name)
    return jsonify({"message": "Song deleted from playlist!"}), 200


@user_blueprint.route("/get-all-playlists", methods=["GET"])
@token_required
def get_all_playlists(user_id):
    """
    Get all playlists
    params:
        user_id: id of user
    return:
        playlists: list of playlist objects
    """
    playlists = user_service.get_all_playlists(user_id)
    return jsonify({"playlists": playlists}), 200


@user_blueprint.route("/get-playlist-by-name", methods=["GET"])
@token_required
def get_playlist_by_name(user_id):
    """
    Get playlist by name
    params:
        playlist_name: name of playlist
    return:
        playlist: playlist object
    """
    data = request.get_json()
    if not data or not "playlist_name" in data:
        raise BadRequest("Missing playlist_name in the request body")
    playlist_name = data["playlist_name"]
    playlist = user_service.get_playlist_by_name(user_id, playlist_name)
    if playlist:
        return jsonify({"playlist": playlist}), 200
    else:
        return jsonify({"message": "Playlist not found"}), 404


@user_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    """Handle bad request"""
    return jsonify(error=str(e.description)), 400


@user_blueprint.errorhandler(NotFound)
def handle_not_found(e):
    """Handle not found"""
    return jsonify(error=str(e.description)), 404

# search song by name, its artist and album 
@user_blueprint.route('/search_songs', methods=['GET'])
@token_required
def search_songs(user_id):
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400
    try:
        songs = song_service.search_songs(query)
        return jsonify(songs), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500