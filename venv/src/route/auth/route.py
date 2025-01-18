# auth_route.py
from flask import Blueprint, jsonify, request
from service.firebase_service import get_request_auth_token, authenticate_user, register_user, logoff_user
from firebase_admin import auth

auth_route = Blueprint('auth_route', __name__)

@auth_route.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        user = authenticate_user(email, password)
        return jsonify({"user": user}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401


@auth_route.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not email or not password or not name:
        return jsonify({"error": "Name, email, and password are required"}), 400

    try:
        user = register_user(name, email, password)
        return jsonify({"user": user}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 500


@auth_route.route("/logoff", methods=["POST"])
def logoff():
    try:
        user_id = get_request_auth_token(request)
        logoff_user(user_id)
        return jsonify({"status": "success"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
