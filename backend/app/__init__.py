from flask import Flask
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv
import os

load_dotenv()  

def create_app():
    app = Flask(__name__)

    cred = credentials.Certificate(os.environ.get('FIREBASE_ADMINSDK_JSON_PATH'))
    initialize_app(cred)

    from .routes import init_app
    init_app(app)

    return app
