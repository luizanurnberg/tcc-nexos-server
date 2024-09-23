from flask import Blueprint, jsonify, request

release_route = Blueprint('release_route', __name__)

@release_route.route('/release/insert', methods=['POST'])
def inser_next_release():
    data = request.get_json()

    project_name = data.get('projectName')
    project_description = data.get('projectDescription')
    project_budget = data.get('projectBudget')
    project_select_time = data.get('projectSelectTime')
    requirements = data.get('requirements')
    dependency_matrix = data.get('dependencyMatrix')
    number_of_req = data.get('numberOfReq')
    number_of_clients = data.get('numberOfClients')

    return jsonify({"message": "success", "projectName": project_name})
