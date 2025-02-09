import pytest
from unittest.mock import MagicMock, patch
from persistence.mongo_repository import MongoRepository

@pytest.fixture
def mock_collection():
    return MagicMock()

@pytest.fixture
def repository(mock_collection, app):
    with app.app_context():
        with patch('flask.current_app.db', {'test_collection': mock_collection}):
            repo = MongoRepository('test_collection')
            yield repo

def test_insert_one(repository, mock_collection):
    # Arrange
    document = {"name": "John", "age": 30}
    mock_collection.insert_one.return_value.inserted_id = "12345"

    # Act
    result = repository.insert_one(document)

    # Assert
    mock_collection.insert_one.assert_called_once_with(document)
    assert result == "12345"


def test_insert_many(repository, mock_collection):
    # Arrange
    documents = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 22}]
    mock_collection.insert_many.return_value.inserted_ids = ["123", "456"]

    # Act
    result = repository.insert_many(documents)

    # Assert
    mock_collection.insert_many.assert_called_once_with(documents)
    assert result == ["123", "456"]


def test_find_one(repository, mock_collection):
    # Arrange
    query = {"name": "John"}
    mock_collection.find_one.return_value = {"name": "John", "age": 30}

    # Act
    result = repository.find_one(query)

    # Assert
    mock_collection.find_one.assert_called_once_with(query)
    assert result == {"name": "John", "age": 30}


def test_find_many(repository, mock_collection):
    # Arrange
    query = {"age": {"$gt": 20}}
    mock_collection.find.return_value.limit.return_value = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 22}
    ]

    # Act
    result = repository.find_many(query)

    # Assert
    mock_collection.find.assert_called_once_with(query)
    mock_collection.find.return_value.limit.assert_called_once_with(0)
    assert result == [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 22}]


def test_update_one(repository, mock_collection):
    # Arrange
    query = {"name": "John"}
    update_values = {"age": 31}
    mock_collection.update_one.return_value.modified_count = 1

    # Act
    result = repository.update_one(query, update_values)

    # Assert
    mock_collection.update_one.assert_called_once_with(query, {"$set": update_values})
    assert result == 1


def test_delete_one(repository, mock_collection):
    # Arrange
    query = {"name": "John"}
    mock_collection.delete_one.return_value.deleted_count = 1

    # Act
    result = repository.delete_one(query)

    # Assert
    mock_collection.delete_one.assert_called_once_with(query)
    assert result == 1
