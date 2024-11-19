from model.release import ReleaseModel
from persistence.mongo_repository import MongoRepository
from flask import current_app


class ReleaseService:
    def __init__(self):
        self.release_repository = MongoRepository("Release")

    def create_release(self, data):
        release = ReleaseModel.from_dict(data)
        return self.release_repository.insert_one(release.to_dict())
