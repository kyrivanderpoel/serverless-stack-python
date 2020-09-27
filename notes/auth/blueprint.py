import boto3
from os import environ
import json

from flask import Blueprint, jsonify, request, session

from ..exception import validate_arguments
from .model import User
from .adapter import CognitoUserAdapter


client_id = environ["COGNITO_CLIENT_ID"]
pool_id = environ["COGNITO_POOL_ID"]
cognito_idp_client = boto3.client("cognito-idp")
user_adapter = CognitoUserAdapter(client_id=client_id, pool_id=pool_id, cognito_idp_client=cognito_idp_client)
auth_api = Blueprint("auth_api", __name__)


@auth_api.route("/login", methods=["POST"])
def login():
    json_data = request.json or {}
    user_id = json_data.get("user_id")
    password = json_data.get("password")

    validate_arguments(user_id=user_id, password=password)

    user = User(user_id=user_id, password=password)
    auth_dict = user_adapter.login(user)
    session["auth"] = auth_dict
    return jsonify(message=f"Login successful for {user_id}.")

@auth_api.route("/logout", methods=["POST"])
def logout():
    user_adapter.check_auth(session.get("auth", {}))
    json_data = request.json or {}
    user_id = json_data.get("user_id")
    validate_arguments(user_id=user_id)

    user = User(user_id=user_id)
    user_adapter.logout(session["auth"])

    return jsonify(message=f"Logout successful for {user_id}.")


@auth_api.route("/user", methods=["GET"])
def list_users():
    users = user_adapter.all()
    return jsonify(users=[user.to_json_dict() for user in users])


@auth_api.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    user = user_adapter.find(user_id=user_id)
    return jsonify(user=user.to_json_dict())


@auth_api.route("/user", methods=["POST"])
def create_user():
    json_data = request.json or {}
    user_id = json_data.get("user_id")
    password = json_data.get("password")
    validate_arguments(user_id=user_id, password=password)

    user = User(user_id=user_id, password=password)
    user_adapter.save(user)

    return jsonify(user=user.to_json_dict())

@auth_api.route("/user/<user_id>/confirm", methods=["POST"])
def confirm():
    # This route should go away, but it is very handy for testing.
    validate_arguments(user_id=user_id)

    user = User(user_id=user_id)
    user_adapter.admin_confirm_signup(user)

    return jsonify(message=f"Confirmed account for {user_id}.")
