# TODO: Implement a client!
import json
import requests
from flask.cli import AppGroup
import click

from ..auth.client import AuthClient

note_cli = AppGroup("note", help="manage notes")
note_endpoint = "http://localhost:5000/v1/note"
auth_client = AuthClient()


@note_cli.command("create")
@click.option("--user-id", required=True)
@click.option("--password", required=True)
@click.option("--attachment", required=True)
@click.option("--content", required=True)
def create_note(user_id, password, attachment, content):
    with auth_client.authenticated_session(user_id, password) as s:
        response = s.post(note_endpoint, json=dict(user_id=user_id, attachment=attachment, content=content))
    print(json.dumps(response.json(), indent=2))

@note_cli.command("update")
@click.option("--user-id", required=True)
@click.option("--note-id", required=True)
@click.option("--password", required=True)
@click.option("--attachment", required=False)
@click.option("--content", required=False)
def update_note(user_id, note_id, password, attachment, content):
    with auth_client.authenticated_session(user_id, password) as s:
        # 2. Update the note
        endpoint = note_endpoint + f"/{user_id}/{note_id}"
        response = s.put(endpoint, json=dict(attachment=attachment, content=content))
    print(json.dumps(response.json(), indent=2))

@note_cli.command("list")
@click.option("--user-id", required=True)
@click.option("--password", required=True)
def list_notes(user_id, password):
    with auth_client.authenticated_session(user_id, password) as s:
        url = note_endpoint + f"/{user_id}"
        response = session.get(url)
    print(json.dumps(response.json(), indent=2))

@note_cli.command("get")
@click.option("--user-id", required=True)
@click.option("--note-id", required=True)
@click.option("--password", required=True)
def get_note(user_id, note_id, password):
    with auth_client.authenticated_session(user_id, password) as s:
        url = note_endpoint + f"/{user_id}/{note_id}"
        response = session.get(url)
        print(json.dumps(response.json(), indent=2))
