from flask import Blueprint, request, jsonify, make_response
from werkzeug.exceptions import NotFound, BadRequest
from functools import wraps
from app.services.artist_service import ArtistService


artist_blueprint = Blueprint('artist', __name__)
artist_service = ArtistService()


@artist_blueprint.route('/get_by_name/<artist_name>', methods=['GET'])
def get_artist_by_name(artist_name):
    artist = artist_service.get_artist_by_name(artist_name)
    if artist is None:
        raise NotFound(f'Artist with name {artist_name} not found.')
    return jsonify({'artist': artist.to_dict()}), 200

@artist_blueprint.route('/create', methods=['POST'])
def create_artist():
    data = request.get_json()
    if not data or not all(k in data for k in ('Name', 'Genres', 'Image', 'Popularity', 'Albums')):
        raise BadRequest('Missing name, description, or image_url.')

    artist_id = artist_service.create_artist(data['Name'], data['Genres'], data['Image'], data['Popularity'], data['Albums'])
    if not artist_id:
        raise NotFound('Could not create artist.')

    return jsonify({'message': 'New artist created!', 'artist_id': artist_id}), 201

@artist_blueprint.route('/<artist_id>', methods=['GET'])
def get_artist(artist_id):
    artist = artist_service.get_artist_by_id(artist_id)
    if artist is None:
        raise NotFound('Artist not found.')
    return jsonify({'artist': artist.to_dict()}), 200

@artist_blueprint.route('/<artist_id>', methods=['PUT'])
def update_artist(artist_id):
    data = request.get_json()
    if not data:
        raise BadRequest('No data provided for update.')
    artist_service.update_artist(artist_id, data)
    return jsonify({'message': 'Artist updated!'}), 200

@artist_blueprint.route('/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    artist_service.delete_artist(artist_id)
    return jsonify({'message': 'Artist deleted!'}), 200

@artist_blueprint.route('/all', methods=['GET'])
def get_all_artists():
    artist_ids = artist_service.get_all_artist_ids()
    return jsonify({'artist_ids': artist_ids}), 200

@artist_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify(error=str(e.description)), 400

@artist_blueprint.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify(error=str(e.description)), 404
