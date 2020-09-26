import boto3
from os import environ
import json
from flask import Blueprint, jsonify, request, current_app, session

from .model import Note
from .adapter import DynamoDBNoteAdapter
from ..exception import validate_arguments
from ..auth.blueprint import user_adapter


table_name = environ.get("NOTES_DEV_TABLE_NAME", "notes-dev")
dynamodb_resource = boto3.resource("dynamodb")
note_adapter = DynamoDBNoteAdapter(dynamodb_resource=dynamodb_resource, table_name=table_name)

note_api = Blueprint("note_api", __name__)

@note_api.route("", methods=["POST"])
def create_note():
    user_adapter.check_auth(session.get("auth", {}))
    json_data = request.json or {}
    attachment = json_data.get("attachment")
    content = json_data.get("content")
    user_id = json_data.get("user_id")

    # Raise a 400 error if any of the arguments are missing.
    validate_arguments(attachment=attachment, content=content, user_id=user_id)

    note = Note(user_id=user_id, content=content, attachment=attachment)

    note_adapter.save(note)

    return jsonify(note=note.to_json_dict())


@note_api.route("/<user_id>", methods=["GET"])
def list_notes(user_id):
    user_adapter.check_auth(session.get("auth", {}))
    validate_arguments(user_id=user_id)

    notes = note_adapter.filter(user_id=user_id)

    return jsonify(notes=[note.to_json_dict() for note in notes])

@note_api.route("/<user_id>/<note_id>", methods=["GET"])
def get_note(user_id, note_id):
    user_adapter.check_auth(session.get("auth", {}))
    validate_arguments(user_id=user_id, note_id=note_id)

    note = note_adapter.find(user_id=user_id, note_id=note_id)

    return jsonify(note=note.to_json_dict())

@note_api.route("/<user_id>/<note_id>", methods=["PUT"])
def update_note(user_id, note_id):
    user_adapter.check_auth(session.get("auth", {}))
    json_data = request.json or {}
    validate_arguments(user_id=user_id, note_id=note_id)

    user_adapter.check_auth(session.get("auth", {}))
    note = note_adapter.find(user_id=user_id, note_id=note_id)
    note = note_adapter.update(
        note,
        attachment=json_data.get("attachment", note.attachment),
        content=json_data.get("content", note.content),
    )

    return jsonify(message="Note was updated.", note=note.to_json_dict())
