from persistence.mongo_repository import MongoRepository

def list_all_requirements(self, release_id):
    try:
        self.release_repository = MongoRepository("Release")
        query = {"ID": str(release_id)}
        return self.release_repository.find_one(query)
    except Exception as e:
        raise RuntimeError(f"Error listing all requirements: {e}")
