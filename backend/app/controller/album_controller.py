from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import NotFound, BadRequest
from app.services.album_service import AlbumService


album_blueprint = Blueprint("album", __name__)
album_service = AlbumService()


@album_blueprint.route("/create", methods=["POST"])
def create_album():
    """
    Create album
    params:
        Name: name of album
        Image: image of album
        Release Date: release date of album
        Total Tracks: total tracks of album
        Songs: songs of album
        Artists: artists of album
    return:
        message: message of success
        album_id: id of album
    """
    data = request.get_json()
    if not data or not all(
        k in data
        for k in ("Name", "Image", "Release Date", "Total Tracks", "Songs", "Artists")
    ):
        raise BadRequest("Missing required fields.")

    release_date = data.get("Release Date")
    try:
        release_date = datetime.strptime(release_date, "%Y-%m-%d")
    except ValueError:
        raise BadRequest("Invalid release_date format. Use ISO 8601 format.")

    album_id = album_service.create_album(
        data["Name"],
        data["Image"],
        release_date,
        data["Total Tracks"],
        data["Songs"],
        data["Artists"],
    )
    if not album_id:
        raise NotFound("Could not create album.")

    return jsonify({"message": "New album created!", "album_id": album_id}), 201


@album_blueprint.route("/get_by_name/<album_name>", methods=["GET"])
def get_album_by_name(album_name):
    """
    Get album by name
    params:
        album_name: name of album
    return:
        album: album object
    """
    album = album_service.get_album_by_name(album_name)
    if album is None:
        raise NotFound("Album not found.")
    return jsonify({"album": album.to_dict()}), 200


@album_blueprint.route("/<album_id>", methods=["GET"])
def get_album(album_id):
    """
    Get album by id
    params:
        album_id: id of album
    return:
        album: album object
    """
    album = album_service.get_album_by_id(album_id)
    if album is None:
        raise NotFound("Album not found.")
    return jsonify({"album": album.to_dict()}), 200


@album_blueprint.route("/<album_id>", methods=["PUT"])
def update_album(album_id):
    """
    Update album
    params:
        album_id: id of album
        Name: name of album
        Image: image of album
        Release Date: release date of album
        Total Tracks: total tracks of album
        Songs: songs of album
        Artists: artists of album
    return:
        message: message of success
    """
    data = request.get_json()
    if not data:
        raise BadRequest("No data provided for update.")

    album_service.update_album(album_id, data)
    return jsonify({"message": "Album updated!"}), 200


@album_blueprint.route("/<album_id>", methods=["DELETE"])
def delete_album(album_id):
    """
    Delete album
    params:
        album_id: id of album
    return:
        message: message of success
    """
    album_service.delete_album(album_id)
    return jsonify({"message": "Album deleted!"}), 200


@album_blueprint.route("/all", methods=["GET"])
def get_all_album_ids():
    """
    Get all album ids
    params:
        None
    return:
        album_ids: list of album ids
    """
    album_ids = album_service.get_all_album_ids()
    return jsonify({"album_ids": album_ids}), 200


@album_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    """Handle bad request"""
    return jsonify(error=str(e.description)), 400


@album_blueprint.errorhandler(NotFound)
def handle_not_found(e):
    """Handle not found"""
    return jsonify(error=str(e.description)), 404
