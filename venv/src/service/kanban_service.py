from persistence.mongo_repository import MongoRepository

class KanbanService:
    def list_all_requirements(self, release_id):
        self.release_repository = MongoRepository("Release")
        query = {"ID": str(release_id)}
        return self.release_repository.find_one(query)
