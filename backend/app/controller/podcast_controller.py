from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import NotFound, BadRequest
from app.services.podcast_service import PodcastService

podcast_blueprint = Blueprint("podcast", __name__)
podcast_service = PodcastService()

@podcast_blueprint.route("/get-podcasts", methods=["GET"])
def get_all_podcasts():
    return jsonify(podcast_service.get_podcasts()), 200

"""
@podcast_blueprint.route("/get-podcast", methods=["GET"])
def get_podcast_by_name():
    data = request.get_json()
    if "podcast_name" not in data:
        raise BadRequest("Podcast Name is required")
    podcast = podcast_service.get_podcast(data["podcast_name"])
    if podcast is None:
        raise NotFound("Podcast not found")
    return jsonify(podcast), 200
"""

@podcast_blueprint.route("/get-podcast", methods=["GET"])
def get_podcast_by_name():
    podcast_name = request.args.get('podcast_name')
    if not podcast_name:
        return jsonify({"error": "Podcast Name is required"}), 400
    podcast = podcast_service.get_podcast(podcast_name)
    if podcast is None:
        return jsonify({"error": "Podcast not found"}), 404
    return jsonify(podcast), 200


# add a new podcast, name
@podcast_blueprint.route("/add-podcast", methods=["POST"])
def add_podcast():
    data = request.get_json()
    if "name" not in data:
        raise BadRequest("Name is required")
    podcast = podcast_service.create_podcast(data["name"], [])
    return jsonify(podcast), 200

# add a new episode to a podcast
@podcast_blueprint.route("/add-episode", methods=["POST"])
def add_episode():
    data = request.get_json()
    if "episode_name" not in data:
        raise BadRequest("Episode Name is required")
    if "duration" not in data:
        raise BadRequest("Duration is required")
    if "podcast_name" not in data:
        raise BadRequest("Podcast name is required")
    if "description" not in data:
        raise BadRequest("Description is required")
    episode = podcast_service.create_episode(data["podcast_name"], data["episode_name"], data["duration"], data["description"])
    return jsonify(episode.to_dict()), 200

# delete a podcast
@podcast_blueprint.route("/delete-podcast", methods=["POST"])
def delete_podcast():
    data = request.get_json()
    if "id" not in data:
        raise BadRequest("Podcast id is required")
    podcast = podcast_service.delete_podcast(data["id"])
    return jsonify(podcast), 200