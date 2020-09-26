# todo: implement a client wrapping requests.Session
import json
import requests
from flask.cli import AppGroup
import click

auth_cli = AppGroup("auth", help="manage auth")
auth_endpoint = "http://localhost:5000/v1/auth"


@auth_cli.command("create-user")
@click.option("--email", required=True)
@click.option("--password", required=True)
def create_user(email, password):
    endpoint = auth_endpoint + "/user"
    response = requests.post(endpoint, json=dict(user_id=email, password=password))
    print(json.dumps(response.json(), indent=2))


@auth_cli.command("login")
@click.option("--email", required=True)
@click.option("--password", required=True)
def login(email, password):
    endpoint = auth_endpoint + "/login"
    response = requests.post(endpoint, json=dict(user_id=email, password=password))
    print(json.dumps(response.json(), indent=2))

@auth_cli.command("demo-logout")
@click.option("--email", required=True)
@click.option("--password", required=True)
def logout(email, password):
    session = requests.Session()
    # 1. Login
    endpoint = auth_endpoint + "/login"
    response = session.post(endpoint, json=dict(user_id=email, password=password))
    print(json.dumps(response.json(), indent=2))
    # 2. Logout
    endpoint = auth_endpoint + "/logout"
    response = session.post(endpoint, json=dict(user_id=email))
    print(json.dumps(response.json(), indent=2))


@auth_cli.command("confirm")
@click.option("--email", required=True)
def confirm(email):
    endpoint = auth_endpoint + "/confirm"
    response = requests.post(endpoint, json=dict(user_id=email))
    print(json.dumps(response.json(), indent=2))


@auth_cli.command("list-users")
def list_users():
    endpoint = auth_endpoint + "/user"
    response = requests.get(endpoint)
    print(json.dumps(response.json(), indent=2))


@auth_cli.command("get-user")
@click.option("--email", required=True)
def get_user(email):
    endpoint = auth_endpoint + f"/user/{email}"
    response = requests.get(endpoint)
    print(json.dumps(response.json(), indent=2))
