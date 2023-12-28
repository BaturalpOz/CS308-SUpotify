from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import NotFound, BadRequest
from app.services.song_service import SongService

song_blueprint = Blueprint("song", __name__)
song_service = SongService()


@song_blueprint.route("/songs", methods=["POST"])
def add_song():
    """
    Add song
    params:
        Name: name of song
        Duration: duration of song
        Danceability: danceability of song
        Energy: energy of song
        Loudness: loudness of song
        Tempo: tempo of song
        Albums: albums of song
        Artists: artists of song
    return:
        message: message of success
        song_id: id of song
    """
    data = request.get_json()
    if not data or not all(
        k in data
        for k in (
            "Name",
            "Duration",
            "Danceability",
            "Energy",
            "Loudness",
            "Tempo",
            "Albums",
            "Artists",
        )
    ):
        return jsonify({"message": "Missing song information."}), 400

    try:
        song_id = song_service.add_song(
            data["Name"],
            data["Duration"],
            data["Danceability"],
            data["Energy"],
            data["Loudness"],
            data["Tempo"],
            data["Albums"],
            data["Artists"],
        )
        return jsonify({"message": "New song created!", "song_id": song_id}), 201
    except Exception as e:
        return jsonify({"message": "Could not create song.", "error": str(e)}), 500


@song_blueprint.route("/<song_id>", methods=["GET"])
def get_song(song_id):
    """
    Get song by id
    params:
        song_id: id of song
    return:
        song: song object
    """
    song = song_service.get_song_by_id(song_id)
    if song is None:
        raise NotFound("Song not found.")
    return jsonify({"song": song.to_dict()}), 200


@song_blueprint.route("/get_by_name/<song_name>", methods=["GET"])
def get_song_by_name(song_name):
    """
    Get song by name
    params:
        song_name: name of song
    return:
        song: song object
    """
    song = song_service.get_song_by_name(song_name)
    if song is None:
        raise NotFound("Song not found.")
    return jsonify({"song": song.to_dict()}), 200


@song_blueprint.route("/songs/<song_id>", methods=["PUT"])
def update_song(song_id):
    """
    Update song
    params:
        song_id: id of song
        Name: name of song
        Duration: duration of song
        Danceability: danceability of song
        Energy: energy of song
        Loudness: loudness of song
        Tempo: tempo of song
        Albums: albums of song
        Artists: artists of song
    return:
        message: message of success
    """
    data = request.get_json()

    try:
        song_service.update_song(song_id, data)
        return jsonify({"message": "Song updated!"}), 200
    except Exception as e:
        return jsonify({"message": "Could not update song.", "error": str(e)}), 500


@song_blueprint.route("/songs/<song_id>", methods=["DELETE"])
def delete_song(song_id):
    """
    Delete song
    params:
        song_id: id of song
    return:
        message: message of success
    """
    try:
        song_service.delete_song(song_id)
        return jsonify({"message": "Song deleted!"}), 200
    except Exception as e:
        return jsonify({"message": "Could not delete song.", "error": str(e)}), 500


@song_blueprint.route("/all/ids", methods=["GET"])
def get_all_song_ids():
    """
    Get all song ids
    params:
        None
    return:
        song_ids: list of song ids
    """
    song_ids = song_service.get_all_song_ids()
    return jsonify({"song_ids": song_ids}), 200

@song_blueprint.route("/all", methods=["GET"])
def get_all_songs():
    songs = song_service.get_all_songs_with_ids()
    return jsonify({"Songs":songs},200)

@song_blueprint.route("/count",methods=["GET"])
def get_song_count():
    return jsonify({"Number of songs":song_service.get_song_count()})


@song_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    """Handle bad request"""
    return jsonify(error=str(e.description)), 400


@song_blueprint.errorhandler(NotFound)
def handle_not_found(e):
    """Handle not found"""
    return jsonify(error=str(e.description)), 404
