from flask import Blueprint, jsonify, request
from service.kanban_service import list_all_requirements
from bson.json_util import dumps

kanban_route = Blueprint("kanban_route", __name__)

@kanban_route.route("/kanban/list/<release_id>", methods=["GET"])
def list_requirements(release_id):
    try:
        releases = list_all_requirements(release_id)
        return dumps({"message": "success", "data": releases}), 200
    except Exception as e:
        return jsonify({"message": "error", "error": str(e)}), 500
    