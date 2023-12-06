from flask import Blueprint, request, jsonify
from app.services.song_service import SongService  
from datetime import datetime

song_blueprint = Blueprint('song', __name__)
song_service = SongService()  


@song_blueprint.route('/songs', methods=['POST'])
def add_song():
    data = request.get_json()
    if not data or not all(k in data for k in ('Name', 'Duration', 'Danceability', 'Energy', 'Loudness', 'Tempo', 'Albums', 'Artists')):
        return jsonify({'message': 'Missing song information.'}), 400

    try:
        song_id = song_service.add_song(
            data['Name'], data['Duration'], data['Danceability'],
            data['Energy'], data['Loudness'], data['Tempo'],
            data['Albums'], data['Artists'])
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

@song_blueprint.route('/all', methods=['GET'])
def get_all_song_ids():
    song_ids = song_service.get_all_song_ids()
    return jsonify({'song_ids': song_ids}), 200
