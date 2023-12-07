from flask import Flask
import firebase_admin
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv
import os
from flask_cors import CORS

from .controller.user_controller import user_blueprint
from .controller.artist_controller import artist_blueprint
from .controller.album_controller import album_blueprint
from .controller.song_controller import song_blueprint

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.environ.get('FIREBASE_ADMINSDK_JSON_PATH'))
        initialize_app(cred)
    
    CORS(app)

    from .routes import init_app

    init_app(app)

    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(artist_blueprint, url_prefix='/artist')
    app.register_blueprint(album_blueprint, url_prefix='/album')
    app.register_blueprint(song_blueprint, url_prefix='/song')
    return app
