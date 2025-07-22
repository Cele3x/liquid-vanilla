import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
import mongomock
from datetime import datetime, UTC

from src.main import app
from src.database import get_db


class AsyncMongoDB:
    """Mock async MongoDB client for testing."""
    
    def __init__(self):
        self.client = mongomock.MongoClient()
        self.db = self.client.get_database("testRecipeDB")
        
    def __getitem__(self, collection_name):
        return AsyncMongoCollection(self.db[collection_name])


class AsyncMongoCollection:
    """Mock async MongoDB collection for testing."""
    
    def __init__(self, collection):
        self.collection = collection
    
    async def insert_one(self, document):
        result = self.collection.insert_one(document)
        mock_result = AsyncMock()
        mock_result.inserted_id = result.inserted_id
        return mock_result
    
    async def find_one(self, query):
        return self.collection.find_one(query)
    
    async def find_one_and_update(self, query, update):
        return self.collection.find_one_and_update(query, update)
    
    async def find_one_and_delete(self, query):
        return self.collection.find_one_and_delete(query)
    
    async def update_one(self, query, update):
        result = self.collection.update_one(query, update)
        mock_result = AsyncMock()
        mock_result.modified_count = result.modified_count
        return mock_result
    
    async def count_documents(self, query):
        return self.collection.count_documents(query)
    
    def find(self, query=None):
        if query is None:
            query = {}
        return AsyncMongoCursor(self.collection.find(query))
    
    async def aggregate(self, pipeline):
        return list(self.collection.aggregate(pipeline))


class AsyncMongoCursor:
    """Mock async MongoDB cursor for testing."""
    
    def __init__(self, cursor):
        self.cursor = cursor
    
    def skip(self, n):
        return AsyncMongoCursor(self.cursor.skip(n))
    
    def limit(self, n):
        return AsyncMongoCursor(self.cursor.limit(n))
    
    def sort(self, key_or_dict, direction=None):
        if isinstance(key_or_dict, dict):
            # Handle MongoDB sort dict format like { "usageCount": -1 }
            items = list(key_or_dict.items())
            if items:
                key, direction = items[0]
                return AsyncMongoCursor(self.cursor.sort(key, direction))
        else:
            return AsyncMongoCursor(self.cursor.sort(key_or_dict, direction))
        return self
    
    async def to_list(self, length):
        return list(self.cursor)


_test_db = None

async def get_test_db():
    """Get test database connection."""
    global _test_db
    if _test_db is None:
        _test_db = AsyncMongoDB()
    yield _test_db


@pytest.fixture
def mock_image_storage_service():
    """Mock image storage service for testing."""
    mock_service = AsyncMock()
    mock_service.store_image.return_value = {
        "stored_image_path": "/test/path/image.jpg",
        "stored_image_url": "/api/v1/images/test_image.jpg", 
        "image_stored_at": datetime.now(UTC).isoformat()
    }
    return mock_service


@pytest.fixture
def client(mock_image_cache_service):
    """Test client with mocked database and image service."""
    global _test_db
    _test_db = None  # Reset database for each test
    
    app.dependency_overrides[get_db] = get_test_db
    
    with patch('src.recipes.routers.image_cache_service', mock_image_cache_service):
        with TestClient(app) as test_client:
            yield test_client
    
    app.dependency_overrides.clear()
    _test_db = None  # Clean up after test
