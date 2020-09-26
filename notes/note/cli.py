# TODO: Implement a client!
import json
import requests
from flask.cli import AppGroup
import click

from ..auth.cli import auth_endpoint

note_cli = AppGroup("note", help="manage notes")
note_endpoint = "http://localhost:5000/v1/note"

@note_cli.command("create")
@click.option("--user-id", required=True)
@click.option("--password", required=True)
@click.option("--attachment", required=True)
@click.option("--content", required=True)
def create_note(user_id, password, attachment, content):
    session = requests.Session()
    # 1. Login
    endpoint = auth_endpoint + "/login"
    response = session.post(endpoint, json=dict(user_id=user_id, password=password))
    print(json.dumps(response.json(), indent=2))

    # 2. Create the note
    response = session.post(note_endpoint, json=dict(user_id=user_id, attachment=attachment, content=content))
    print(json.dumps(response.json(), indent=2))

    # 3. Logout
    endpoint = auth_endpoint + "/logout"
    response = session.post(endpoint, json=dict(user_id=user_id))
    print(json.dumps(response.json(), indent=2))

@note_cli.command("update")
@click.option("--user-id", required=True)
@click.option("--note-id", required=True)
@click.option("--password", required=True)
@click.option("--attachment", required=False)
@click.option("--content", required=False)
def update_note(user_id, note_id, password, attachment, content):
    session = requests.Session()
    # 1. Login
    endpoint = auth_endpoint + "/login"
    response = session.post(endpoint, json=dict(user_id=user_id, password=password))
    print(json.dumps(response.json(), indent=2))

    # 2. Update the note
    endpoint = note_endpoint + f"/{user_id}/{note_id}"
    response = session.put(endpoint, json=dict(attachment=attachment, content=content))
    print(json.dumps(response.json(), indent=2))

    # 3. Logout
    endpoint = auth_endpoint + "/logout"
    response = session.post(endpoint, json=dict(user_id=user_id))
    print(json.dumps(response.json(), indent=2))


@note_cli.command("list")
@click.option("--user-id", required=True)
@click.option("--password", required=True)
def list_notes(user_id, password):
    session = requests.Session()

    # 1. Login
    endpoint = auth_endpoint + "/login"
    response = session.post(endpoint, json=dict(user_id=user_id, password=password))
    print(json.dumps(response.json(), indent=2))

    # 2. List the notes
    url = note_endpoint + f"/{user_id}"
    response = session.get(url)
    print(json.dumps(response.json(), indent=2))

    # 3. Logout
    endpoint = auth_endpoint + "/logout"
    response = session.post(endpoint, json=dict(user_id=user_id))
    print(json.dumps(response.json(), indent=2))

@note_cli.command("get")
@click.option("--user-id", required=True)
@click.option("--note-id", required=True)
@click.option("--password", required=True)
def get_note(user_id, note_id, password):
    session = requests.Session()

    # 1. Login
    endpoint = auth_endpoint + "/login"
    response = session.post(endpoint, json=dict(user_id=user_id, password=password))
    print(json.dumps(response.json(), indent=2))

    # 2. Get the note
    url = note_endpoint + f"/{user_id}/{note_id}"
    response = session.get(url)
    print(json.dumps(response.json(), indent=2))

    # 3. Logout
    endpoint = auth_endpoint + "/logout"
    response = session.post(endpoint, json=dict(user_id=user_id))
    print(json.dumps(response.json(), indent=2))
