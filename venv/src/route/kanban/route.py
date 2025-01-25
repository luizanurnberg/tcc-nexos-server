from flask import Blueprint, jsonify
from service.kanban_service import KanbanService
from bson.json_util import dumps

kanban_route = Blueprint("kanban_route", __name__)

@kanban_route.route("/kanban/list/<release_id>", methods=["GET"])
def list_requirements(release_id):
    try:
        kanban_service = KanbanService()
        releases = kanban_service.list_all_requirements(release_id)

        return dumps({"message": "success", "data": releases}), 200
    except Exception as e:
        return jsonify({"message": "error", "error": str(e)}), 500
    