from flask import Blueprint, jsonify

auth_route = Blueprint('auth_route', __name__)

@auth_route.route('/users', methods=['GET'])
def get_users():
    return jsonify({"message": "List of users"})
