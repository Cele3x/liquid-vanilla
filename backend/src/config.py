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
    ALLOWED_REQUEST_URLS: list = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://192.168.178.78",
        "https://liquid-vanilla.com",
    ]

    MONGO_HOST: str = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT: int = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER: str = urllib.parse.quote_plus(os.getenv("MONGO_USER", ""))
    MONGO_PASSWORD: str = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD", ""))
    MONGO_DATABASE: str = os.getenv("MONGO_DATABASE", "RecipeDB")
    # Construct MongoDB URL with or without authentication
    if MONGO_USER and MONGO_PASSWORD:
        MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE}"
    else:
        MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE}"

    IMAGE_STORAGE_DIR: str = os.getenv("IMAGE_STORAGE_DIR", str(Path(__file__).parent / "static" / "images" / "recipes"))


settings = Settings()
