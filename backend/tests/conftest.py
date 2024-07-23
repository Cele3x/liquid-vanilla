import pytest
from pymongo import MongoClient
from fastapi.testclient import TestClient

from src.config import settings
from src.main import app
from src.database import get_db


def get_test_db_client():
    return MongoClient(settings.MONGO_URL)


async def get_test_db():
    test_db_client = get_test_db_client()
    test_db = test_db_client.get_database("testRecipesDB")
    yield test_db


def drop_test_db():
    test_db_client = get_test_db_client()
    test_db_client.drop_database("testRecipesDB")
    test_db_client.close()


@pytest.fixture
def client():
    settings.MONGO_URL = 'mongodb://localhost:27017/'
    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    drop_test_db()
