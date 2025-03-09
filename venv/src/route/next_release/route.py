from bson.json_util import dumps
from flask import Blueprint, jsonify, request
from service.next_release_service import run_heuristic
from service.pre_process_instance_service import initialize_data, transformation1
from service.release_service import ReleaseService
from service.firebase_service import get_request_auth_token

release_route = Blueprint("release_route", __name__)

@release_route.route("/release/insert", methods=["POST"])
def insert_next_release():
    try:
        get_request_auth_token(request)
        
        data = request.get_json()

        # Inicializa os dados e executa a transformação
        instance = initialize_data(data)
        transformation1(instance)
        project_select_time = data.get("projectSelectTime")

        # Cria a base da release
        release_service = ReleaseService()
        release = release_service.create_release(data, instance)

        # Executa o algoritmo
        solution, selected_customers = run_heuristic(
            instance["Q"],
            instance["w"],
            instance["c"],
            instance["b"],
            instance["n"],
            instance["m"],
            0.11,
            0.38,
            0.5,
            project_select_time,
        )

        # Atualiza o registro com os dados gerados
        release["CLIENT_CHOSEN"] = release_service.filter_clients_chosen(
            release, selected_customers
        )
        release["REQUIREMENT_TO_IMPLEMENT"] = (
            release_service.filter_requirements_to_implement(release, solution)
        )
        release["STATUS"] = {"ID": 2, "NAME": "Concluído"}
        release_service.update_release(release)

        return jsonify(
            {
                "message": "success",
                "projectName": data.get("projectName"),
            },
            200,
        )
    except Exception as e:
        if release:
            release["STATUS"] = {
                "ID": 3,
                "NAME": "Erro",
            }
            release_service.update_release(release)

        return (
            jsonify(
                {
                    "message": "error",
                    "error": str(e),
                    "projectName": data.get("projectName"),
                }
            ),
            500,
        )


@release_route.route("/release/list", methods=["GET"])
def list_releases():
    try:
        get_request_auth_token(request)
        
        uid = request.args.get('uid')
        if not uid:
            return jsonify({"message": "UID não fornecido"}), 400
        
        release_service = ReleaseService()
        releases = release_service.list_all_releases(uid)

        return dumps({"message": "success", "data": releases}), 200
    except Exception as e:
        return jsonify({"message": "error", "error": str(e)}), 500
    

@release_route.route("/release/delete/<release_id>", methods=["DELETE"])
def delete_release(release_id):
    try:
        get_request_auth_token(request)
        release_service = ReleaseService()
        deleted_count = release_service.delete_release(release_id)

        if deleted_count:
            return jsonify({"message": "success", "deleted_count": deleted_count}), 200
        else:
            return jsonify({"message": "not_found", "error": "Release not found"}), 404
    except Exception as e:
        return jsonify({"message": "error", "error": str(e)}), 500
    
