from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import NotFound, BadRequest
from app.services.podcast_service import PodcastService

podcast_blueprint = Blueprint("podcast", __name__)
podcast_service = PodcastService()

@podcast_blueprint.route("/get-podcasts", methods=["GET"])
def get_all_podcasts():
    return jsonify(podcast_service.get_all_podcasts())

@podcast_blueprint.route("/get-podcast", methods=["POST"])
def get_podcast_by_id():
    data = request.get_json()
    if "podcast_name" not in data:
        raise BadRequest("Podcast ID is required")
    podcast = podcast_service.get_podcast(data["podcast_name"])
    if podcast is None:
        raise NotFound("Podcast not found")
    return jsonify(podcast)

# add a new podcast, name
@podcast_blueprint.route("/add-podcast", methods=["POST"])
def add_podcast():
    data = request.get_json()
    if "name" not in data:
        raise BadRequest("Name is required")
    podcast = podcast_service.create_podcast(data["name"], [])
    return jsonify(podcast)

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
    episode = podcast_service.create_episode(data["podcast_name"], data["episode_name"], data["duration"])
    return jsonify(episode)