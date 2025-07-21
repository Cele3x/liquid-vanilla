from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
from bson import ObjectId, errors as bson_errors

from .models import Recipe
from .schemas import serialize_recipe, serialize_recipes
from ..database import get_db
from ..utils import convert_object_ids
from ..images.service import image_cache_service


router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"],
)
collection = "recipes"


@router.get("/recommendations", status_code=status.HTTP_200_OK)
async def get_recipe_recommendations(
        db: AsyncIOMotorClient = Depends(get_db),
        locked_ids: Optional[str] = Query(None, description="Comma-separated list of locked recipe IDs")
) -> Dict[str, Any]:
    """
    Get 8 random recipe recommendations that have at least one image.
    Locked recipes will be kept in their positions and new random recipes will fill remaining slots.
    
    :param db: Database connection
    :param locked_ids: Comma-separated string of recipe IDs to keep locked in place
    :returns: Dictionary containing recommended recipes
    """
    try:
        locked_recipe_ids = []
        if locked_ids:
            locked_recipe_ids = [id.strip() for id in locked_ids.split(",") if id.strip()]
        
        locked_recipes = []
        
        # Get locked recipes if any
        if locked_recipe_ids:
            try:
                # Convert to ObjectIds for query
                object_ids = [ObjectId(id) for id in locked_recipe_ids if ObjectId.is_valid(id)]
                locked_recipes = await db[collection].find({
                    "_id": {"$in": object_ids}
                }).to_list(len(object_ids))
            except Exception as e:
                print(f"Error fetching locked recipes: {e}")
                locked_recipes = []
        
        # Calculate how many new recipes we need
        needed_count = max(0, 8 - len(locked_recipes))
        
        new_recipes = []
        if needed_count > 0:
            # Get random recipes, excluding already locked ones
            exclude_ids = [ObjectId(id) for id in locked_recipe_ids if ObjectId.is_valid(id)]
            
            pipeline = []
            if exclude_ids:
                pipeline.append({"$match": {"_id": {"$nin": exclude_ids}}})
            pipeline.append({"$sample": {"size": needed_count}})
            
            new_recipes = await db[collection].aggregate(pipeline).to_list(needed_count)
        
        # Combine locked and new recipes
        all_recommendations = locked_recipes + new_recipes
        
        return {
            "recommendations": serialize_recipes(all_recommendations)
        }
        
    except Exception as e:
        print(f"Aggregation failed, using fallback: {str(e)}")
        
        # Fallback - get first 8 recipes with images
        try:
            recommendations = await db[collection].find({
                "previewImageUrlTemplate": {"$exists": True, "$ne": "", "$ne": None}
            }).limit(8).to_list(8)
            
            return {
                "recommendations": serialize_recipes(recommendations)
            }
        except:
            return {"recommendations": []}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_recipes(
        db: AsyncIOMotorClient = Depends(get_db),
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(20, le=100, description="Number of items per page"),
        tags: List[str] = Query(
            default=[],
            description="List of tag IDs to filter recipes. Pass multiple times for multiple tags.",
            examples=["?tags=507f1f77bcf86cd799439011&tags=507f1f77bcf86cd799439012"]
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
    @param tags: Optional list of tag IDs to filter recipes (use multiple tag parameters for multiple tags)
    @param search: Optional text to search for
    @return: Dictionary containing recipes and pagination info
    @raise HTTPException: If invalid tag ID format is provided
    """
    skip = (page - 1) * page_size
    query: Dict[str, Any] = {}

    if tags:
        try:
            tag_ids = [ObjectId(tag.strip()) for tag in tags if tag.strip()]
            query["tagIds"] = {"$in": tag_ids}
        except bson_errors.InvalidId as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid tag ID format: {str(e)}"
            )

    if search:
        query["title"] = {"$regex": search, "$options": "i"}

    recipes = await db[collection].find(query).skip(skip).limit(page_size).sort("rating", -1).to_list(page_size)
    print(f"db[${collection}].find({query}).skip({skip}).limit({page_size}).sort('rating', -1)")
    total = await db[collection].count_documents(query)

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
    Creates a new recipe with converted ObjectIds and caches images.

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
        result = await db[collection].insert_one(converted_dict)

        if result.inserted_id:
            recipe_id = str(result.inserted_id)
            
            # Cache image asynchronously if image URL template exists
            if recipe.previewImageUrlTemplate:
                try:
                    image_data = await image_cache_service.cache_image(
                        recipe_id, recipe.previewImageUrlTemplate
                    )
                    
                    # Update recipe with cached image info
                    await db[collection].update_one(
                        {"_id": ObjectId(recipe_id)},
                        {"$set": image_data}
                    )
                except Exception as e:
                    # Log error but don't fail recipe creation
                    print(f"Failed to cache image for recipe {recipe_id}: {str(e)}")
            
            return recipe_id

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
    """
    Get a single recipe by ID and cache its image if not already cached.
    
    :param recipe_id: Recipe ID
    :param db: Database connection
    :returns: Serialized recipe data
    :raises HTTPException: If recipe not found
    """
    recipe = await db[collection].find_one({"_id": ObjectId(recipe_id)})
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Cache image if it exists but isn't cached yet
    if (recipe.get("previewImageUrlTemplate") and 
        not recipe.get("cachedImageUrl")):
        try:
            image_data = await image_cache_service.cache_image(
                recipe_id, recipe["previewImageUrlTemplate"]
            )
            
            # Update recipe with cached image info
            await db[collection].update_one(
                {"_id": ObjectId(recipe_id)},
                {"$set": image_data}
            )
            
            # Update the recipe dict with cached image info
            recipe.update(image_data)
        except Exception as e:
            # Log error but don't fail recipe retrieval
            print(f"Failed to cache image for recipe {recipe_id}: {str(e)}")
    
    return serialize_recipe(recipe)


@router.put("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_recipe(recipe: Recipe, recipe_id: str, db: AsyncIOMotorClient = Depends(get_db)):
    result = await db[collection].find_one_and_update({"_id": ObjectId(recipe_id)}, {"$set": recipe.model_dump()})
    if not result:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(recipe_id: str, db: AsyncIOMotorClient = Depends(get_db)):
    result = await db[collection].find_one_and_delete({"_id": ObjectId(recipe_id)})
    if not result:
        raise HTTPException(status_code=404, detail="Recipe not found")
