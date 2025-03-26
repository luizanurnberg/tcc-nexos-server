from flask import Blueprint, jsonify, request
from service.client_service import ClientService
from service.firebase_service import get_request_auth_token
from bson.json_util import dumps

client_route = Blueprint("client_route", __name__)


@client_route.route("/client/insert", methods=["POST"])
def insert_client():
    try:
        get_request_auth_token(request)
        data = request.get_json()

        client_service = ClientService()
        client = client_service.create_client(data)

        if client:
            return jsonify(
                {
                    "message": "success",
                    "client": data.get("clientName"),
                },
                200,
            )
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "error",
                    "error": str(e),
                    "client": data.get("clientName"),
                }
            ),
            500,
        )


@client_route.route("/client/list/<user_id>", methods=["GET"])
def list_client(user_id):
    try:
        get_request_auth_token(request)
        client_service = ClientService()
        clients = client_service.list_all_clients(user_id)

        return dumps({"message": "success", "data": clients}), 200
    except Exception as e:
        return jsonify({"message": "error", "error": str(e)}), 500

@client_route.route("/client/filter/<client_name>/<user_id>", methods=["GET"])
def list_client_by_name(client_name, user_id):
    try:
        get_request_auth_token(request)
        client_service = ClientService()
        clients = client_service.filter_clients_by_name(client_name, user_id)
        clients_without_id = []
        if clients:
            for client in clients:
                client_dict = client.copy() 
                client_dict.pop('_id', None)
                clients_without_id.append(client_dict)
        return jsonify({"message": "success", "data": clients_without_id}), 200
    except Exception as e:
        return jsonify({"message": "error", "error": str(e)}), 500

@client_route.route("/client/update", methods=["POST"])
def update_client():
    try:
        get_request_auth_token(request)
        data = request.get_json()
        client_service = ClientService()
        clients = client_service.update_client(data)

        return dumps({"message": "success", "data": clients}), 200
    except Exception as e:
        return jsonify({"message": "error", "error": str(e)}), 500


@client_route.route("/client/delete/<client_id>", methods=["DELETE"])
def delete_release(client_id):
    try:
        get_request_auth_token(request)
        client_service = ClientService()
        deleted_count = client_service.delete_client(client_id)

        if deleted_count:
            return jsonify({"message": "success", "deleted_count": deleted_count}), 200
        else:
            return jsonify({"message": "not_found", "error": "Client not found"}), 404
    except Exception as e:
        return jsonify({"message": "error", "error": str(e)}), 500
