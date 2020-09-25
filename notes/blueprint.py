import boto3
from os import environ
import json
from flask import Blueprint, jsonify, request, current_app

from .model import Note
from .persistor import Persistor, DynamoDBAdapter
from .exception import validate_arguments


table_name = environ.get("NOTES_DEV_TABLE_NAME", "notes-dev")
dynamodb_resource = boto3.resource("dynamodb")
database_adapter = DynamoDBAdapter(dynamodb_resource=dynamodb_resource, table_name=table_name)
persistor = Persistor(database_adapter=database_adapter)

v1_api = Blueprint("v1_api", __name__)

@v1_api.route("/note", methods=["POST"])
def create_note():
    json_data = request.json or {}
    attachment = json_data.get("attachment")
    content = json_data.get("content")
    user_id = json_data.get("user_id")
    if request.environ.get("serverless.event"):
        user_id = request.environ["serverless.event"]["requestContext"]["identity"]["cognitoIdentity"]

    # Raise a 400 error if any of the arguments are missing.
    validate_arguments(attachment=attachment, content=content, user_id=user_id)

    note = Note(user_id=user_id, content=content, attachment=attachment)

    persistor.save(note)

    return jsonify(note=note.to_json_dict())


@v1_api.route("/note/<user_id>", methods=["GET"])
def list_notes(user_id):
    # Raise a 400 error if any of the arguments are missing.
    validate_arguments(user_id=user_id)

    notes = persistor.filter_by(Note, user_id=user_id)

    return jsonify(notes=[note.to_json_dict() for note in notes])

@v1_api.route("/note/<user_id>/<note_id>", methods=["GET"])
def get_note(user_id, note_id):
    # Raise a 400 error if any of the arguments are missing.
    validate_arguments(user_id=user_id, note_id=note_id)

    note = persistor.find(Note, user_id=user_id, note_id=note_id)

    return jsonify(note=note.to_json_dict())
