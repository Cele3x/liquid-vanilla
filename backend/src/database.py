from motor.motor_asyncio import AsyncIOMotorClient

from .config import settings


async def get_client():
    client = AsyncIOMotorClient(settings.MONGO_URL)
    return client


async def check_connection():
    client = await get_client()
    try:
        conn = await client.server_info()
        print(f'Connected to MongoDB {conn.get("version")} on {settings.MONGO_URL}!')
    except Exception as e:
        print(f'Could not connect to MongoDB: {e}')
    finally:
        client.close()


async def get_db():
    client = await get_client()
    try:
        database = settings.MONGO_DATABASE
        yield client.get_database(database)
    except Exception as e:
        print(f'Could not connect to MongoDB: {e}')
    finally:
        client.close()
