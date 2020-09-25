from os import environ
from flask import Flask, request, jsonify
from .blueprint import v1_api
from .exception import ERROR_HANDLERS
from .util import ISOFormatJSONEncoder
from .cli import CLIS


app = Flask(__name__)

app.register_blueprint(v1_api, url_prefix="/v1")
for cls, error_handler in ERROR_HANDLERS.items():
    app.register_error_handler(cls, error_handler)
for cli in CLIS:
    app.cli.add_command(cli)
app.json_encoder = ISOFormatJSONEncoder
