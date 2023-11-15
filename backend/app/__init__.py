from flask import Flask
import firebase_admin
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv
import os

from .controller.user_controller import user_blueprint

load_dotenv()  

def create_app():
    app = Flask(__name__)

    if not firebase_admin._apps:
        cred = credentials.Certificate(os.environ.get('FIREBASE_ADMINSDK_JSON_PATH'))
        initialize_app(cred)

    from .routes import init_app

    init_app(app)

    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app
