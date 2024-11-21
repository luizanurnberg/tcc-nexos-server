from model.release import ReleaseModel
from persistence.mongo_repository import MongoRepository
from flask import current_app


class ReleaseService:
    def __init__(self):
        self.release_repository = MongoRepository("Release")

    def create_release(self, data, instance):
        release = ReleaseModel.from_dict(data, instance)
        self.release_repository.insert_one(release.to_dict())

        return release.to_dict()

    def update_release(self, data):
        query = {"ID": data.get("ID")}
        update_values = {k: v for k, v in data.items() if k != "ID"}
        return self.release_repository.update_one(query, update_values)

    def filter_requirements_to_implement(self, release, solution):
        # Filtra os requisitos que devem ser implementados com base na solução.

        requirements = release.get("REQUIREMENT", [])
        requirements_to_implement = []

        for i, req in enumerate(requirements):
            if i < len(solution) and solution[i] == 1:
                requirements_to_implement.append(req)

        return requirements_to_implement

    def filter_clients_chosen(self, release, selected_customers):
        # Filtra os clientes que devem ser implementados com base na solução.
        
        all_clients = release.get("CLIENT", [])
        selected_clients = [
            client for client in all_clients if client["ID"] in selected_customers
        ]
        return selected_clients
    
    def list_all_releases(self):
        self.release_repository = MongoRepository("Release")
        return self.release_repository.find_many()
    
    def delete_release(self, release_id):
        query = {"ID": release_id}
        return self.release_repository.delete_one(query)


