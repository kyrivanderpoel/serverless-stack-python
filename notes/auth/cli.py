# todo: implement a client wrapping requests.Session
import json
import requests
from flask.cli import AppGroup
import click

from .client import AuthClient

auth_cli = AppGroup("auth", help="manage auth")
auth_client = AuthClient()


@auth_cli.command("create-user")
@click.option("--email", required=True)
@click.option("--password", required=True)
def create_user(email, password):
    response = auth_client.create_user(email, password)
    print(json.dumps(response.json(), indent=2))


@auth_cli.command("login")
@click.option("--email", required=True)
@click.option("--password", required=True)
def login(email, password):
    response = auth_client.login(email, password)
    print(json.dumps(response.json(), indent=2))

@auth_cli.command("demo-logout")
@click.option("--email", required=True)
@click.option("--password", required=True)
def logout(email, password):
    # 1. Login
    response = auth_client.login(email, password)
    print(json.dumps(response.json(), indent=2))

    # 2. Logout
    response = auth_client.logout(email)
    print(json.dumps(response.json(), indent=2))


@auth_cli.command("confirm")
@click.option("--email", required=True)
def confirm(email):
    response = auth_client.confirm(email)
    print(json.dumps(response.json(), indent=2))


@auth_cli.command("list-users")
def list_users():
    response = auth_client.list_users()
    print(json.dumps(response.json(), indent=2))


@auth_cli.command("get-user")
@click.option("--email", required=True)
def get_user(email):
    response = auth_client.get_user(email)
    print(json.dumps(response.json(), indent=2))
