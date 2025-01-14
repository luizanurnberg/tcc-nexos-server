from flask import current_app

class MongoRepository:
    def __init__(self, collection_name):
        self.collection = current_app.db[collection_name]

    def insert_one(self, document):
        """Insere um único documento na coleção."""
        try:
            return self.collection.insert_one(document).inserted_id
        except Exception as e:
            current_app.logger.error(f"Error in insert_one: {e}")
            raise

    def insert_many(self, documents):
        """Insere múltiplos documentos na coleção."""
        try:
            return self.collection.insert_many(documents).inserted_ids
        except Exception as e:
            current_app.logger.error(f"Error in insert_many: {e}")
            raise

    def find_one(self, query):
        """Encontra um único documento na coleção."""
        try:
            return self.collection.find_one(query)
        except Exception as e:
            current_app.logger.error(f"Error in find_one: {e}")
            raise

    def find_many(self, query=None, limit=0):
        """Encontra múltiplos documentos na coleção."""
        try:
            if query is None:
                query = {}
            return list(self.collection.find(query).limit(limit))
        except Exception as e:
            current_app.logger.error(f"Error in find_many: {e}")
            raise

    def update_one(self, query, update_values):
        """Atualiza um único documento na coleção."""
        try:
            return self.collection.update_one(
                query, {"$set": update_values}
            ).modified_count
        except Exception as e:
            current_app.logger.error(f"Error in update_one: {e}")
            raise

    def update_many(self, query, update_values):
        """Atualiza múltiplos documentos na coleção."""
        try:
            return self.collection.update_many(
                query, {"$set": update_values}
            ).modified_count
        except Exception as e:
            current_app.logger.error(f"Error in update_many: {e}")
            raise

    def delete_one(self, query):
        """Deleta um único documento da coleção."""
        try:
            return self.collection.delete_one(query).deleted_count
        except Exception as e:
            current_app.logger.error(f"Error in delete_one: {e}")
            raise

    def delete_many(self, query):
        """Deleta múltiplos documentos da coleção."""
        try:
            return self.collection.delete_many(query).deleted_count
        except Exception as e:
            current_app.logger.error(f"Error in delete_many: {e}")
            raise
