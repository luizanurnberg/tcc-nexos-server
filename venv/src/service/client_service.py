from model.client import ClientModel
from persistence.mongo_repository import MongoRepository
from flask import current_app

class ClientService:
    def __init__(self):
        try:
            self.client_repository = MongoRepository("Client")
        except Exception as e:
            raise RuntimeError(f"Error initializing ClientService: {e}")

    def create_client(self, data):
        try:
            client = ClientModel.from_dict(data)
            self.client_repository.insert_one(client.to_dict())
            return client.to_dict()
        except Exception as e:
            raise RuntimeError(f"Error creating client: {e}")

    def update_client(self, data):
        try:
            query = {"ID": data.get("ID")}
            update_values = {k: v for k, v in data.items() if k != "ID"}
            return self.client_repository.update_one(query, update_values)
        except Exception as e:
            raise RuntimeError(f"Error updating client: {e}")

    def filter_clients_by_name(self, release, selected_customers):
        try:
            all_clients = release.get("CLIENT", [])
            selected_clients = [
                client for client in all_clients if client["ID"] in selected_customers
            ]
            return selected_clients
        except Exception as e:
            raise RuntimeError(f"Error filtering clients chosen: {e}")

    def list_all_clients(self, uid):
        try:
            self.client_repository = MongoRepository("Client")
            return self.client_repository.find_many({"CREATED_BY_ID": uid})
        except Exception as e:
            raise RuntimeError(f"Error listing all clients: {e}")

    def delete_client(self, client_id):
        try:
            query = {"ID": client_id}
            return self.client_repository.delete_one(query)
        except Exception as e:
            raise RuntimeError(f"Error deleting client: {e}")
