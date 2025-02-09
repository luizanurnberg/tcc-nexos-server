import pytest
from bson.json_util import dumps

# Fixture que realiza login e retorna os headers de autenticação para os testes
@pytest.fixture
def auth_headers(client):
    login_data = {"email": "test@example.com", "password": "password123"}
    login_response = client.post("/login", json=login_data)
    assert login_response.status_code == 200
    token = login_response.json["user"]["idToken"]
    return {"Authorization": f"Bearer {token}"}


def test_list_releases_success(client, auth_headers):
    # Testa se a listagem de releases retorna sucesso quando um UID válido é fornecido
    response = client.get("/release/list?uid=YRT4hdSkpwOtuD6XmpMsoSBdN403", headers=auth_headers)
    assert response.status_code == 200


def test_list_releases_missing_uid(client, auth_headers):
    # Testa o comportamento da API quando o UID não é informado na requisição
    response = client.get("/release/list", headers=auth_headers)
    assert response.status_code == 400
    assert response.json["message"] == "UID não fornecido"


def test_delete_release_success(client, auth_headers):
    # Testa se a exclusão de um release retorna sucesso ou 'not found', dependendo da existência do release
    release_id = "test_release_123"
    response = client.delete(f"/release/delete/{release_id}", headers=auth_headers)
    assert response.status_code in [200, 404]  # Pode ser sucesso ou não encontrado
    
    if response.status_code == 200:
        assert response.json["message"] == "success"
        assert "deleted_count" in response.json
    else:
        assert response.json["message"] == "not_found"