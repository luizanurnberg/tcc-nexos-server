import pytest
from unittest.mock import patch

def test_list_requirements_valid_id(client):
    release_id = "1732304024374142883"
    response = client.get(f'/kanban/list/{release_id}')  
    assert response.status_code == 200

def test_list_requirements_invalid_id(client):
    release_id = "invalid_release_id"
    with patch('service.kanban_service.KanbanService.list_all_requirements') as mock_list_all_requirements:
        mock_list_all_requirements.side_effect = Exception("Invalid release ID")
        response = client.get(f'/kanban/list/{release_id}')
        assert response.status_code == 500
        assert "error" in response.json
