from model.release import ReleaseModel
from persistence.mongo_repository import MongoRepository
from flask import current_app

class ReleaseService:
    def __init__(self):
        try:
            self.release_repository = MongoRepository("Release")
        except Exception as e:
            raise RuntimeError(f"Error initializing ReleaseService: {e}")

    def create_release(self, data, instance):
        try:
            release = ReleaseModel.from_dict(data, instance)
            self.release_repository.insert_one(release.to_dict())
            return release.to_dict()
        except Exception as e:
            raise RuntimeError(f"Error creating release: {e}")

    def update_release(self, data):
        try:
            query = {"ID": data.get("ID")}
            update_values = {k: v for k, v in data.items() if k != "ID"}
            return self.release_repository.update_one(query, update_values)
        except Exception as e:
            raise RuntimeError(f"Error updating release: {e}")

    def filter_requirements_to_implement(self, release, solution):
        try:
            requirements = release.get("REQUIREMENT", [])
            requirements_to_implement = []

            for i, req in enumerate(requirements):
                if i < len(solution) and solution[i] == 1:
                    requirements_to_implement.append(req)

            return requirements_to_implement
        except Exception as e:
            raise RuntimeError(f"Error filtering requirements to implement: {e}")

    def filter_clients_chosen(self, release, selected_customers):
        try:
            all_clients = release.get("CLIENT", [])
            
            selected_clients = [
                client for client in all_clients if client["ID"] in selected_customers
            ]
            
            unique_clients = []
            seen_codes = set()
            
            for client in selected_clients:
                code = client.get("CODE")
                if code not in seen_codes:
                    unique_clients.append(client)
                    seen_codes.add(code)
            
            return unique_clients
        except Exception as e:
            raise RuntimeError(f"Error filtering clients chosen: {e}")

    def list_all_releases(self, uid):
        try:
            self.release_repository = MongoRepository("Release")
            return self.release_repository.find_many({"CREATED_BY_ID": uid})
        except Exception as e:
            raise RuntimeError(f"Error listing all releases: {e}")

    def delete_release(self, release_id):
        try:
            query = {"ID": release_id}
            return self.release_repository.delete_one(query)
        except Exception as e:
            raise RuntimeError(f"Error deleting release: {e}")

    def get_release_metrics(self, user_id):
        aggregated_data = self.release_repository.aggregate_release_metrics(user_id)
        
        metrics = []
        for month_data in aggregated_data:
            client_cards = {}
            for client_info in month_data['clients']:
                for client in client_info['client']:
                    client_id = client['ID']
                    if client_id not in client_cards:
                        client_cards[client_id] = {
                            'name': client['NAME'],
                            'total_cards': 0
                        }
                    client_cards[client_id]['total_cards'] += client_info['cards']
            
            metrics.append({
                'year': month_data['_id']['year'],
                'month': month_data['_id']['month'],
                'total_value': month_data['total_value'],
                'total_releases': month_data['total_releases'],
                'finished_releases': month_data['finished_releases'],
                'generation_releases': month_data['generation_releases'],
                'error_releases': month_data['error_releases'],
                'clients': list(client_cards.values())
            })
        
        return metrics
