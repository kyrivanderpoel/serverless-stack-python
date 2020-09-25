from os import environ
import json
import requests
from flask.cli import AppGroup
import click

note_cli = AppGroup("note", help="manage notes")
endpoint = environ.get("LOCAL_API_ENDPOINT", "http://localhost:5000/v1/note")

@note_cli.command("create")
@click.option("--user-id", required=True)
@click.option("--attachment", required=True)
@click.option("--content", required=True)
def create_note(user_id, attachment, content):
    response = requests.post(endpoint, json=dict(user_id=user_id, attachment=attachment, content=content))
    print(json.dumps(response.json(), indent=2))


@note_cli.command("list")
@click.option("--user-id", required=True)
def list_notes(user_id):
    url = endpoint + f"/{user_id}"
    response = requests.get(url)
    print(json.dumps(response.json(), indent=2))

CLIS = [note_cli]


@note_cli.command("get")
@click.option("--user-id", required=True)
@click.option("--note-id", required=True)
def get_note(user_id, note_id):
    url = endpoint + f"/{user_id}/{note_id}"
    response = requests.get(url)
    print(json.dumps(response.json(), indent=2))

CLIS = [note_cli]
