from flask import Blueprint, jsonify, request
# from service.next_release_service import run_heuristic
from service.pre_process_instance_service import initialize_data

release_route = Blueprint('release_route', __name__)

@release_route.route('/release/insert', methods=['POST'])
def inser_next_release():
    data = request.get_json()

    # Initialize instance data using the received JSON
    instance = initialize_data(data)
    # transformation1(instance)

    # Execute heuristic algorithm
    # solution, total_cost, selected_customers, best_iteration, best_obj_value, elapsed_time = run_heuristic(
    #     instance['Q'], instance['w'], instance['c'], instance['b'], 
    #     instance['n'], instance['m'], 0.11, 0.38, 0.5
    # )

    return jsonify({
        "message": "success",
        "projectName": data.get('projectName'),
        # "solution": solution,
        # "totalCost": total_cost,
        # "selectedCustomers": selected_customers,
        # "bestIteration": best_iteration,
        # "objectiveValue": best_obj_value,
        # "executionTime": elapsed_time
    })
