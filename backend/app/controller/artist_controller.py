from flask import Blueprint, request, jsonify, make_response
from werkzeug.exceptions import NotFound, BadRequest
from functools import wraps
from app.services.artist_service import ArtistService

# Blueprint setup
artist_blueprint = Blueprint('artist', __name__)
artist_service = ArtistService()

# Authentication decorator (if needed)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Implement authentication logic if necessary
        # You can use this decorator to protect certain endpoints with authentication
        return f(*args, **kwargs)
    return decorated

@artist_blueprint.route('/get_by_name/<artist_name>', methods=['GET'])
@token_required
def get_artist_by_name(artist_name):
    artist = artist_service.get_artist_by_name(artist_name)
    if artist is None:
        raise NotFound(f'Artist with name {artist_name} not found.')
    return jsonify({'artist': artist.to_dict()}), 200

@artist_blueprint.route('/create', methods=['POST'])
@token_required
def create_artist():
    data = request.get_json()
    if not data or not all(k in data for k in ('Name', 'Genres', 'Image', 'Popularity', 'Albums')):
        raise BadRequest('Missing name, description, or image_url.')

    artist_id = artist_service.create_artist(data['Name'], data['Genres'], data['Image'], data['Popularity'], data['Albums'])
    if not artist_id:
        raise NotFound('Could not create artist.')

    return jsonify({'message': 'New artist created!', 'artist_id': artist_id}), 201

@artist_blueprint.route('/<artist_id>', methods=['GET'])
@token_required
def get_artist(artist_id):
    artist = artist_service.get_artist_by_id(artist_id)
    if artist is None:
        raise NotFound('Artist not found.')
    return jsonify({'artist': artist.to_dict()}), 200

@artist_blueprint.route('/<artist_id>', methods=['PUT'])
@token_required
def update_artist(artist_id):
    data = request.get_json()
    if not data:
        raise BadRequest('No data provided for update.')
    artist_service.update_artist(artist_id, data)
    return jsonify({'message': 'Artist updated!'}), 200

@artist_blueprint.route('/<artist_id>', methods=['DELETE'])
@token_required
def delete_artist(artist_id):
    artist_service.delete_artist(artist_id)
    return jsonify({'message': 'Artist deleted!'}), 200

@artist_blueprint.route('/all', methods=['GET'])
@token_required
def get_all_artists():
    artist_ids = artist_service.get_all_artist_ids()
    return jsonify({'artist_ids': artist_ids}), 200

@artist_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify(error=str(e.description)), 400

@artist_blueprint.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify(error=str(e.description)), 404
