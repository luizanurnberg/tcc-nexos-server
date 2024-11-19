from flask import Blueprint, jsonify, request
from service.next_release_service import run_heuristic
from service.pre_process_instance_service import initialize_data, transformation1
from service.release_service import ReleaseService

release_route = Blueprint("release_route", __name__)


@release_route.route("/release/insert", methods=["POST"])
def inser_next_release():

    data = request.get_json()
    release_service = ReleaseService()
    release_id = release_service.create_release(data)

    print(release_id)

    instance = initialize_data(data)
    transformation1(instance)
    project_select_time = data.get("projectSelectTime")

    solution, total_cost, selected_customers, best_obj_value = run_heuristic(
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

    return jsonify(
        {
            "message": "success",
            "projectName": data.get("projectName"),
            "solution": solution,
            "totalCost": total_cost,
            "selectedCustomers": selected_customers,
            "objectiveValue": best_obj_value,
        }
    )
