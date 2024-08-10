import pymongo
from pymongo import MongoClient, errors

from config import settings


async def get_client():
    client = MongoClient(settings.MONGO_URL)
    return client


async def check_connection():
    client = await get_client()
    try:
        conn = client.server_info()
        print(f'Connected to MongoDB {conn.get("version")} on {settings.MONGO_URL}!')
    except pymongo.errors.ConnectionFailure as e:
        print(f'Could not connect to MongoDB: {e}')
    except Exception as e:
        print(f'Exception: {e}')
    finally:
        client.close()


async def get_db():
    client = await get_client()
    try:
        database = settings.MONGO_DATABASE
        yield client.get_database(database)
    except pymongo.errors.ConnectionFailure as e:
        print(f'Could not connect to MongoDB: {e}')
    finally:
        client.close()
