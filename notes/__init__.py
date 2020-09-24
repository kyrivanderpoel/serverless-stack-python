from flask import Flask
from .blueprint import v1_api

app = Flask(__name__)

app.register_blueprint(v1_api, url_prefix="/v1")
