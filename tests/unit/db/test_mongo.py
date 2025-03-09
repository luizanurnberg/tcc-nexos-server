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

# Test for insert_one
def test_insert_one(repository, mock_collection):
    # Arrange
    document = {"name": "John", "age": 30}
    mock_collection.insert_one.return_value.inserted_id = "12345"

    # Act
    result = repository.insert_one(document)

    # Assert
    mock_collection.insert_one.assert_called_once_with(document)
    assert result == "12345"

def test_insert_one_error(repository, mock_collection):
    # Arrange
    document = {"name": "John", "age": 30}
    mock_collection.insert_one.side_effect = Exception("Database error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        repository.insert_one(document)
    assert str(exc_info.value) == "Database error"
    mock_collection.insert_one.assert_called_once_with(document)

# Test for insert_many
def test_insert_many(repository, mock_collection):
    # Arrange
    documents = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 22}]
    mock_collection.insert_many.return_value.inserted_ids = ["123", "456"]

    # Act
    result = repository.insert_many(documents)

    # Assert
    mock_collection.insert_many.assert_called_once_with(documents)
    assert result == ["123", "456"]

def test_insert_many_error(repository, mock_collection):
    # Arrange
    documents = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 22}]
    mock_collection.insert_many.side_effect = Exception("Database error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        repository.insert_many(documents)
    assert str(exc_info.value) == "Database error"
    mock_collection.insert_many.assert_called_once_with(documents)

# Test for find_one
def test_find_one(repository, mock_collection):
    # Arrange
    query = {"name": "John"}
    mock_collection.find_one.return_value = {"name": "John", "age": 30}

    # Act
    result = repository.find_one(query)

    # Assert
    mock_collection.find_one.assert_called_once_with(query)
    assert result == {"name": "John", "age": 30}

def test_find_one_not_found(repository, mock_collection):
    # Arrange
    query = {"name": "NonExistent"}
    mock_collection.find_one.return_value = None

    # Act
    result = repository.find_one(query)

    # Assert
    mock_collection.find_one.assert_called_once_with(query)
    assert result is None

def test_find_one_error(repository, mock_collection):
    # Arrange
    query = {"name": "John"}
    mock_collection.find_one.side_effect = Exception("Database error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        repository.find_one(query)
    assert str(exc_info.value) == "Database error"
    mock_collection.find_one.assert_called_once_with(query)

# Test for find_many
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

def test_find_many_default_args(repository, mock_collection):
    # Arrange
    mock_collection.find.return_value.limit.return_value = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 22}
    ]

    # Act
    result = repository.find_many()

    # Assert
    mock_collection.find.assert_called_once_with({})
    mock_collection.find.return_value.limit.assert_called_once_with(0)
    assert result == [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 22}]

def test_find_many_with_limit(repository, mock_collection):
    # Arrange
    query = {"age": {"$gt": 20}}
    mock_collection.find.return_value.limit.return_value = [
        {"name": "Alice", "age": 25}
    ]

    # Act
    result = repository.find_many(query, limit=1)

    # Assert
    mock_collection.find.assert_called_once_with(query)
    mock_collection.find.return_value.limit.assert_called_once_with(1)
    assert result == [{"name": "Alice", "age": 25}]

def test_find_many_error(repository, mock_collection):
    # Arrange
    query = {"age": {"$gt": 20}}
    mock_collection.find.side_effect = Exception("Database error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        repository.find_many(query)
    assert str(exc_info.value) == "Database error"
    mock_collection.find.assert_called_once_with(query)

# Test for update_one
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

def test_update_one_error(repository, mock_collection):
    # Arrange
    query = {"name": "John"}
    update_values = {"age": 31}
    mock_collection.update_one.side_effect = Exception("Database error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        repository.update_one(query, update_values)
    assert str(exc_info.value) == "Database error"
    mock_collection.update_one.assert_called_once_with(query, {"$set": update_values})

# Test for update_many
def test_update_many(repository, mock_collection):
    # Arrange
    query = {"age": {"$gt": 20}}
    update_values = {"status": "active"}
    mock_collection.update_many.return_value.modified_count = 2

    # Act
    result = repository.update_many(query, update_values)

    # Assert
    mock_collection.update_many.assert_called_once_with(query, {"$set": update_values})
    assert result == 2

def test_update_many_error(repository, mock_collection):
    # Arrange
    query = {"age": {"$gt": 20}}
    update_values = {"status": "active"}
    mock_collection.update_many.side_effect = Exception("Database error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        repository.update_many(query, update_values)
    assert str(exc_info.value) == "Database error"
    mock_collection.update_many.assert_called_once_with(query, {"$set": update_values})

# Test for delete_one
def test_delete_one(repository, mock_collection):
    # Arrange
    query = {"name": "John"}
    mock_collection.delete_one.return_value.deleted_count = 1

    # Act
    result = repository.delete_one(query)

    # Assert
    mock_collection.delete_one.assert_called_once_with(query)
    assert result == 1

def test_delete_one_error(repository, mock_collection):
    # Arrange
    query = {"name": "John"}
    mock_collection.delete_one.side_effect = Exception("Database error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        repository.delete_one(query)
    assert str(exc_info.value) == "Database error"
    mock_collection.delete_one.assert_called_once_with(query)

# Test for delete_many
def test_delete_many(repository, mock_collection):
    # Arrange
    query = {"status": "inactive"}
    mock_collection.delete_many.return_value.deleted_count = 3

    # Act
    result = repository.delete_many(query)

    # Assert
    mock_collection.delete_many.assert_called_once_with(query)
    assert result == 3

def test_delete_many_no_matches(repository, mock_collection):
    # Arrange
    query = {"status": "inactive"}
    mock_collection.delete_many.return_value.deleted_count = 0

    # Act
    result = repository.delete_many(query)

    # Assert
    mock_collection.delete_many.assert_called_once_with(query)
    assert result == 0

def test_delete_many_error(repository, mock_collection):
    # Arrange
    query = {"status": "inactive"}
    mock_collection.delete_many.side_effect = Exception("Database error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        repository.delete_many(query)
    assert str(exc_info.value) == "Database error"
    mock_collection.delete_many.assert_called_once_with(query)