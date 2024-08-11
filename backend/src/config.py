import os
from dotenv import load_dotenv
from pathlib import Path
import urllib.parse

env_path = Path(__file__).parents[2] / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Recipe API"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_DESCRIPTION: str = "A RESTful API for managing recipes"

    BASE_URL: str = "/api/v1"
    ALLOWED_REQUEST_URLS: str = ["http://localhost", "http://localhost:8000", "http://localhost:5173"]

    MONGO_HOST: str = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT: int = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER: str = urllib.parse.quote_plus(os.getenv("MONGO_USER", ""))
    MONGO_PASSWORD: str = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD", ""))
    MONGO_DATABASE: str = os.getenv("MONGO_DATABASE", "RecipesDB")
    # MONGO_URL = "mongodb://%s:%s@%s:%s/%s" % (MONGO_USER, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DATABASE)
    MONGO_URL = "mongodb://%s:%s/%s" % (MONGO_HOST, MONGO_PORT, MONGO_DATABASE)


settings = Settings()
