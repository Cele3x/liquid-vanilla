from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.database import check_connection
from src.recipes import routers as recipe_routers
from src.tags import routers as tag_routers
from src.categories import routers as category_routers
from src.images import routers as image_routers


@asynccontextmanager
async def lifespan(_: FastAPI):
    await check_connection()
    yield

# Create an instance of the FastAPI application.
# The application is configured with the project name, description, and version.
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# Add a middleware to the application for handling CORS.
# This middleware allows requests from the defined origins.
# It also allows the sharing of credentials and all HTTP methods and headers.
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=settings.ALLOWED_REQUEST_URLS,  # These are the URLs from which the API will accept requests.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers that handle requests to the API.
app.include_router(recipe_routers.router, prefix=settings.BASE_URL)
app.include_router(tag_routers.router, prefix=settings.BASE_URL)
app.include_router(category_routers.router, prefix=settings.BASE_URL)
app.include_router(image_routers.router, prefix=f"{settings.BASE_URL}/images", tags=["Images"])


# Define a route for the root of the API.
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Willkommen zur Rezept-API!"}


# uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
