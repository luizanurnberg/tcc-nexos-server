import os
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from route.auth.route import auth_route
from route.next_release.route import release_route

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME") 

def create_app():
    app = Flask(__name__)
    CORS(
        app,
        methods=["GET", "POST", "OPTIONS"],
        allow_headers="*",
    )

    app.register_blueprint(auth_route)
    app.register_blueprint(release_route)

    try:
        client = MongoClient(MONGO_URI)
        app.db = client[DATABASE_NAME]
        print(f"Conectado ao banco de dados: {DATABASE_NAME}")
    except Exception as e:
        print("Erro ao conectar ao MongoDB:", e)
        app.db = None

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000)
