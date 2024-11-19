from flask import current_app

class MongoRepository:
    def __init__(self, collection_name):
        self.collection = current_app.db[collection_name]

    def insert_one(self, document):
        """Insere um único documento na coleção."""
        return self.collection.insert_one(document).inserted_id

    def insert_many(self, documents):
        """Insere múltiplos documentos na coleção."""
        return self.collection.insert_many(documents).inserted_ids

    def find_one(self, query):
        """Encontra um único documento na coleção."""
        return self.collection.find_one(query)

    def find_many(self, query=None, limit=0):
        """Encontra múltiplos documentos na coleção."""
        if query is None:
            query = {}
        return list(self.collection.find(query).limit(limit))

    def update_one(self, query, update_values):
        """Atualiza um único documento na coleção."""
        return self.collection.update_one(query, {"$set": update_values}).modified_count

    def update_many(self, query, update_values):
        """Atualiza múltiplos documentos na coleção."""
        return self.collection.update_many(query, {"$set": update_values}).modified_count

    def delete_one(self, query):
        """Deleta um único documento da coleção."""
        return self.collection.delete_one(query).deleted_count

    def delete_many(self, query):
        """Deleta múltiplos documentos da coleção."""
        return self.collection.delete_many(query).deleted_count
