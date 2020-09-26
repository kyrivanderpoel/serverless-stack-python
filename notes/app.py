from os import environ
from flask import Flask, request, jsonify
from .note.blueprint import note_api
from .auth.blueprint import auth_api
from .exception import ERROR_HANDLERS
from .util import ISOFormatJSONEncoder
from .auth.cli import auth_cli
from .note.cli import note_cli


app = Flask(__name__)

app.secret_key = environ["NOTES_APP_SECRET_KEY"]
app.register_blueprint(note_api, url_prefix="/v1/note")
app.register_blueprint(auth_api, url_prefix="/v1/auth")
for cls, error_handler in ERROR_HANDLERS.items():
    app.register_error_handler(cls, error_handler)

# Warning: The CLI is configured to only use the local API client. This is hardcoded.
for cli in [auth_cli, note_cli]:
    app.cli.add_command(cli)

# Formats all datetime.datetime strings into isoformat across the entire application.
app.json_encoder = ISOFormatJSONEncoder
