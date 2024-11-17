from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
from bson import ObjectId, errors as bson_errors

from .models import Recipe
from .schemas import serialize_recipe, serialize_recipes
from src.database import get_db
from src.utils import convert_object_ids


router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"],
)
collection = "recipes"


@router.get("/", status_code=status.HTTP_200_OK)
async def get_recipes(
        db: AsyncIOMotorClient = Depends(get_db),
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(20, le=100, description="Number of items per page"),
        tags: Optional[List[str]] = Query(
            None,
            description="List of tag IDs to filter recipes",
            example=["507f1f77bcf86cd799439011"]
        ),
        search: Optional[str] = Query(
            None,
            description="Search text to filter recipes by title"
        ),
) -> Dict[str, Any]:
    """
    Retrieve paginated recipes with optional tag filtering.

    @param db: Database connection
    @param page: Page number (starting from 1)
    @param page_size: Number of items per page
    @param tags: Optional list of tag IDs to filter recipes
    @param search: Optional text to search for
    @return: Dictionary containing recipes and pagination info
    @raise HTTPException: If invalid tag IDs are provided
    """
    skip = (page - 1) * page_size
    query: Dict[str, Any] = {}

    if tags:
        try:
            tag_ids = [ObjectId(tag) for tag in tags]
            query["tagIds"] = {"$all": tag_ids}
        except bson_errors.InvalidId as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid tag ID format: {str(e)}"
            )

    if search:
        query["title"] = {"$regex": search, "$options": "i"}

    recipes = db[collection].find(query).skip(skip).limit(page_size).sort("rating", -1)
    print(f"db[${collection}].find({query}).skip({skip}).limit({page_size}).sort('rating', -1)")
    total = db[collection].count_documents(query)

    return {
        "recipes": serialize_recipes(recipes),
        "page": page,
        "page_size": page_size,
        "total": total,
        "has_next": (page * page_size) < total,
        "has_previous": page > 1,
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_recipe(
        recipe: Recipe,
        db: AsyncIOMotorClient = Depends(get_db)
) -> str:
    """
    Creates a new recipe with converted ObjectIds.

    @param recipe: Recipe model to create
    @param db: Database connection
    @return: Created recipe ID
    @raise HTTPException: If recipe creation fails
    """
    try:
        recipe_dict = recipe.model_dump()
        fields_to_convert = [
            "tagIds",
            "userId",
            "ingredientGroups.ingredients.ingredientId",
            "ingredientGroups.ingredients.unitId"
        ]

        converted_dict = convert_object_ids(recipe_dict, fields_to_convert)
        result = db[collection].insert_one(converted_dict)

        if result.inserted_id:
            return str(result.inserted_id)

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Recipe creation failed"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{recipe_id}", status_code=status.HTTP_200_OK)
async def get_recipe(recipe_id: str, db: AsyncIOMotorClient = Depends(get_db)):
    recipe = db[collection].find_one({"_id": ObjectId(recipe_id)})
    if recipe:
        return serialize_recipe(recipe)

    raise HTTPException(status_code=404, detail="Recipe not found")


@router.put("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_recipe(recipe: Recipe, recipe_id: str, db: AsyncIOMotorClient = Depends(get_db)):
    result = db[collection].find_one_and_update({"_id": ObjectId(recipe_id)}, {"$set": recipe.model_dump()})
    if not result:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(recipe_id: str, db: AsyncIOMotorClient = Depends(get_db)):
    result = db[collection].find_one_and_delete({"_id": ObjectId(recipe_id)})
    if not result:
        raise HTTPException(status_code=404, detail="Recipe not found")
