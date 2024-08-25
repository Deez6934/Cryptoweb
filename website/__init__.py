from flask import Flask
import config

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.api_key

    return app




