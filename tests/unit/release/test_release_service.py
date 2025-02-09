import pytest
from unittest.mock import MagicMock, patch
from model.release import ReleaseModel
from persistence.mongo_repository import MongoRepository
from service.release_service import ReleaseService

@pytest.fixture
def release_service(app):
    with app.app_context():
        service = ReleaseService()
        yield service

@patch('service.release_service.ReleaseModel')
@patch('service.release_service.MongoRepository')
def test_create_release(mock_repo, mock_model, release_service):
    # Arrange
    mock_data = {"name": "Release 1"}
    mock_instance = MagicMock()
    mock_model.from_dict.return_value = MagicMock(to_dict=lambda: mock_data)
    mock_repo.return_value.insert_one.return_value = None

    # Act
    result = release_service.create_release(mock_data, mock_instance)

    # Assert
    assert result == mock_data

def test_filter_requirements_to_implement(release_service):
    # Arrange
    mock_release = {"REQUIREMENT": ["Req1", "Req2", "Req3"]}
    mock_solution = [1, 0, 1]

    # Act
    result = release_service.filter_requirements_to_implement(mock_release, mock_solution)

    # Assert
    assert result == ["Req1", "Req3"]

def test_filter_clients_chosen(release_service):
    # Arrange
    mock_release = {"CLIENT": [{"ID": "1"}, {"ID": "2"}, {"ID": "3"}]}
    mock_selected_customers = ["1", "3"]

    # Act
    result = release_service.filter_clients_chosen(mock_release, mock_selected_customers)

    # Assert
    assert result == [{"ID": "1"}, {"ID": "3"}]

@patch('service.release_service.MongoRepository')
def test_list_all_releases(mock_repo, release_service):
    # Arrange
    mock_uid = "user123"
    mock_repo.return_value.find_many.return_value = [{"name": "Release 1"}]

    # Act
    result = release_service.list_all_releases(mock_uid)

    # Assert
    assert result == [{"name": "Release 1"}]

@patch('service.release_service.MongoRepository')
def test_init_error(mock_repo):
    # Arrange
    mock_repo.side_effect = Exception("Connection Error")

    # Act & Assert
    with pytest.raises(RuntimeError) as exc_info:
        ReleaseService()
    assert "Error initializing ReleaseService: Connection Error" in str(exc_info.value)