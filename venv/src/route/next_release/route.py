from flask import Blueprint, jsonify, request
from service.next_release_service import run_heuristic
from service.pre_process_instance_service import initialize_data, transformation1
from service.release_service import ReleaseService

release_route = Blueprint("release_route", __name__)


@release_route.route("/release/insert", methods=["POST"])
def inser_next_release():
    try:
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
