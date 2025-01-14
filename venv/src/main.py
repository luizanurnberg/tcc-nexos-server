import os
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

from route.auth.route import auth_route
from route.next_release.route import release_route
from route.kanban.route import kanban_route

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

def create_app():
    app = Flask(__name__)
    CORS(
        app,
        methods=["GET", "POST", "OPTIONS", "DELETE"],
        allow_headers="*",
    )

    app.register_blueprint(auth_route)
    app.register_blueprint(release_route)
    app.register_blueprint(kanban_route)

    # Conexão com MongoDB
    try:
        client = MongoClient(MONGO_URI)
        app.db = client[DATABASE_NAME]
        print(f"Conectado ao banco de dados: {DATABASE_NAME}")
    except Exception as e:
        print("Erro ao conectar ao MongoDB:", e)
        app.db = None

    # Conexão com Firebase
    try:
        cred = credentials.Certificate(FIREBASE_CREDENTIALS)
        firebase_admin.initialize_app(cred)
        app.firebase_api_key = FIREBASE_API_KEY
        print("Conectado ao Firebase")
    except Exception as e:
        print("Erro ao conectar ao Firebase:", e)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000)
