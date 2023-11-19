from flask import Blueprint, request, jsonify
from app.services.song_service import SongService  # Import your SongService
from datetime import datetime

song_blueprint = Blueprint('song', __name__)
song_service = SongService()  # Create an instance of your SongService


@song_blueprint.route('/songs', methods=['POST'])
def add_song():
    data = request.get_json()

    release_date_str = data['release_date']
    release_date = datetime.strptime(release_date_str, '%Y-%m-%dT%H:%M:%SZ')


    try:
        song_id = song_service.add_song(
            data['title'], data['duration'], data['genre'],
            data['language'], data['release_country'],
            release_date,  # Pass the datetime object
            data.get('albums', []), data.get('artists', [])
        )
        return jsonify({'message': 'New song created!', 'song_id': song_id}), 201
    except Exception as e:
        return jsonify({'message': 'Could not create song.', 'error': str(e)}), 500


@song_blueprint.route('/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    song = song_service.get_song_by_id(song_id)
    if song:
        return jsonify({'song': song.to_dict()}), 200
    else:
        return jsonify({'message': 'Song not found.'}), 404


@song_blueprint.route('/songs/<song_id>', methods=['PUT'])
def update_song(song_id):
    data = request.get_json()

    try:
        song_service.update_song(song_id, data)
        return jsonify({'message': 'Song updated!'}), 200
    except Exception as e:
        return jsonify({'message': 'Could not update song.', 'error': str(e)}), 500


@song_blueprint.route('/songs/<song_id>', methods=['DELETE'])
def delete_song(song_id):

    try:
        song_service.delete_song(song_id)
        return jsonify({'message': 'Song deleted!'}), 200
    except Exception as e:
        return jsonify({'message': 'Could not delete song.', 'error': str(e)}), 500
