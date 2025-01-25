import pytest
from unittest.mock import patch
from service.firebase_service import authenticate_user

@pytest.fixture

# LOGIN TEST
def mock_authenticate_user():
    with patch('service.firebase_service.authenticate_user') as mock:
        yield mock

def test_login_success(client):
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    response = client.post('/login', json=login_data)
    assert response.status_code == 200

def test_login_missing_email(client):
    login_data = {
        "password": "password123"
    }
    
    response = client.post('/login', json=login_data)

    assert response.status_code == 400
    assert response.json["error"] == "Email and password are required"

def test_login_invalid_credentials(client, mock_authenticate_user):
    login_data = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }
    
    mock_authenticate_user.side_effect = ValueError("Error authenticating the user: INVALID_LOGIN_CREDENTIALS")
    response = client.post('/login', json=login_data)
    assert response.status_code == 401
    assert response.json["error"] == "Error authenticating the user: INVALID_LOGIN_CREDENTIALS"

def mock_register_user():
    with patch('service.firebase_service.register_user') as mock:
        yield mock

# REGISTER TEST
def test_register_success(client):
    register_data = {
        "name": "Test User",
        "email": "test@example.com.br",
        "password": "password123"
    }

    response = client.post('/register', json=register_data)
    assert response.status_code == 200

def test_register_missing_name(client):
    register_data = {
        "email": "test@example.com.rb",
        "password": "password123"
    }

    response = client.post('/register', json=register_data)
    assert response.status_code == 400
    assert response.json["error"] == "Name, email, and password are required"

def test_register_missing_email(client):
    register_data = {
        "name": "Test User",
        "password": "password123"
    }

    response = client.post('/register', json=register_data)
    assert response.status_code == 400
    assert response.json["error"] == "Name, email, and password are required"
