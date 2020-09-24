from flask import Blueprint, jsonify, request


v1_api = Blueprint("v1_api", __name__)

@v1_api.route("/hello", methods=["GET"])
def hello():
    return jsonify(mesage="Hello!")
