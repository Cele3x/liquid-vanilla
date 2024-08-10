from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
from bson import ObjectId

from .models import Recipe
from .schemas import serialize_recipe, serialize_recipes
from backend.src.database import get_db

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"],
)
collection = "recipes"


@router.get("/", status_code=status.HTTP_200_OK)
async def get_recipes(db: AsyncIOMotorClient = Depends(get_db)):
    recipes = db[collection].find().limit(20)
    return serialize_recipes(recipes)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe: Recipe, db: AsyncIOMotorClient = Depends(get_db)):

    result = db[collection].insert_one(recipe.model_dump())
    if result.inserted_id:
        return str(result.inserted_id)

    raise HTTPException(status_code=422, detail="Recipe not created")


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
