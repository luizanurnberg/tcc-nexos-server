import os
import pytest
from main import create_app
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

@pytest.fixture(scope="session")
def app():
    # Cria a aplicação apenas uma vez para a sessão de testes
    app = create_app({
        "TESTING": True,
        "MONGO_URI": MONGO_URI, 
        "DATABASE_NAME": DATABASE_NAME,
        "FIREBASE_CREDENTIALS": FIREBASE_CREDENTIALS,
        "FIREBASE_API_KEY": FIREBASE_API_KEY
    })
    yield app

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()
