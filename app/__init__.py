# __init__.py or create_app.py

from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os

from .routers.song_router import song_blueprint

load_dotenv()


def create_app():
    app = Flask(__name__)

    try:
        # Attempt to get the Firebase app, and initialize if it doesn't exist
        firebase_admin.get_app()
    except ValueError:
        # Firebase app doesn't exist, initialize it
        try:
            cred = credentials.Certificate(os.environ.get('FIREBASE_ADMINSDK_JSON_PATH'))
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Error initializing Firebase: {e}")

    # Reference to the Firestore Songs collection
    db = firestore.client()
    songs_collection = db.collection('Songs')

    # Store the reference to the Firestore collection in the app context
    app.config['songs_collection'] = songs_collection

    from .routes import init_app
    init_app(app)

    # Register the song blueprint
    app.register_blueprint(song_blueprint, url_prefix='/song')

    return app
