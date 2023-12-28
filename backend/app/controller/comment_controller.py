from flask import Blueprint, request, jsonify
from werkzeug.exceptions import NotFound, BadRequest

from app.services.comment_service import CommentService
from datetime import datetime

comment_blueprint = Blueprint('comment', __name__)
comment_service = CommentService()


@comment_blueprint.route('/send', methods=['POST'])
def send_comment():
    data = request.get_json()
    if not data or not all(k in data for k in ('Commenter', 'Send_Time', 'Comment_Content')):
        return jsonify({'message': 'Missing comment information.'}), 400

    try:
        # Parse 'Send_Time' to datetime
        send_time = datetime.fromisoformat(data['Send_Time'])
        comment_id = comment_service.send_comment(data['Commenter'], data['Comment_Content'], send_time)
        return jsonify({'message': 'New comment sent!', 'comment_id': comment_id}), 201
    except Exception as e:
        return jsonify({'message': 'Could not send comment.', 'error': str(e)}), 500


@comment_blueprint.route('/<comment_id>', methods=['GET'])
def get_comment_by_id(comment_id):
    try:
        comment = comment_service.get_comment(comment_id)
        return jsonify({'comment': comment.to_dict()}), 200
    except ValueError as ve:
        raise NotFound(str(ve))
    except Exception as e:
        return jsonify({'message': 'Could not retrieve comment.', 'error': str(e)}), 500


@comment_blueprint.route('/all', methods=['GET'])
def get_all_comment_ids():
    comment_ids = comment_service.get_all_comment_ids()
    return jsonify({'comment_ids': comment_ids}), 200


@comment_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify(error=str(e.description)), 400


@comment_blueprint.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify(error=str(e.description)), 404
