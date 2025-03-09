import pytest
from unittest.mock import patch
import random
import string

@pytest.fixture
def mock_authenticate_user():
    with patch("service.firebase_service.authenticate_user") as mock:
        yield mock

@pytest.fixture
def mock_register_user():
    with patch("service.firebase_service.register_user") as mock:
        yield mock

@pytest.fixture
def mock_auth_token_and_logoff():
    with patch("service.firebase_service.get_request_auth_token") as mock_token, \
            patch("service.firebase_service.logoff_user") as mock_logoff:
        yield mock_token, mock_logoff

def generate_random_email():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{random_string}@gmail.com"

def test_login_success(client, mock_authenticate_user):
    # Arrange
    login_data = {"email": "test@example.com", "password": "password123"}
    mock_authenticate_user.return_value = {"uid": "123", "email": "test@example.com"}

    # Act
    response = client.post("/login", json=login_data)

    # Assert
    assert response.status_code == 200

def test_login_missing_email(client):
    # Arrange
    login_data = {"password": "password123"}

    # Act
    response = client.post("/login", json=login_data)

    # Assert
    assert response.status_code == 400
    assert response.json == {"error": "Email and password are required"}

def test_login_missing_password(client):
    # Arrange
    login_data = {"email": "test@example.com"}

    # Act
    response = client.post("/login", json=login_data)

    # Assert
    assert response.status_code == 400
    assert response.json == {"error": "Email and password are required"}

def test_login_invalid_credentials(client, mock_authenticate_user):
    # Arrange
    login_data = {"email": "test@example.com", "password": "wrongpassword"}

    # Act
    response = client.post("/login", json=login_data)

    # Assert
    assert response.status_code == 401

def test_register_success(client, mock_register_user):
    # Arrange
    register_data = {
        "name": "Test User",
        "email": generate_random_email(),
        "password": "password123",
    }
    mock_register_user.return_value = {"uid": "123", "email": register_data["email"]}

    # Act
    response = client.post("/register", json=register_data)

    # Assert
    assert response.status_code == 200

def test_register_missing_name(client):
    # Arrange
    register_data = {"email": "test@example.com", "password": "password123"}

    # Act
    response = client.post("/register", json=register_data)

    # Assert
    assert response.status_code == 400
    assert response.json == {"error": "Name, email, and password are required"}

def test_register_missing_email(client):
    # Arrange
    register_data = {"name": "Test User", "password": "password123"}

    # Act
    response = client.post("/register", json=register_data)

    # Assert
    assert response.status_code == 400
    assert response.json == {"error": "Name, email, and password are required"}

def test_register_missing_password(client):
    # Arrange
    register_data = {"name": "Test User", "email": "test@example.com"}

    # Act
    response = client.post("/register", json=register_data)

    # Assert
    assert response.status_code == 400
    assert response.json == {"error": "Name, email, and password are required"}

def test_register_error(client, mock_register_user):
    # Arrange
    register_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
    }

    # Act
    response = client.post("/register", json=register_data)

    # Assert
    assert response.status_code == 500

def test_logout_success(client):
    # Arrange
    login_data = {"email": "test@example.com", "password": "password123"}
    login_response = client.post("/login", json=login_data)
    assert login_response.status_code == 200
    token = login_response.json["user"]["idToken"]

    # Act
    headers = {"Authorization": f"Bearer {token}"}
    logoff_response = client.post("/logoff", headers=headers)
    
    # Assert
    assert logoff_response.status_code == 200
    assert logoff_response.json["status"] == "success"

def test_logoff_missing_token(client):
    # Act
    response = client.post("/logoff")

    # Assert
    assert response.status_code == 500
    assert "error" in response.json

def test_logoff_invalid_token(client, mock_auth_token_and_logoff):
    # Arrange
    mock_token, mock_logoff = mock_auth_token_and_logoff
    mock_token.side_effect = ValueError("Invalid token")

    # Act
    response = client.post("/logoff", headers={"Authorization": "Bearer invalid_token"})

    # Assert
    assert response.status_code == 500