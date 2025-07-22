from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
from bson import ObjectId, errors as bson_errors

from .models import Recipe
from .schemas import serialize_recipe, serialize_recipes
from ..database import get_db
from ..utils import convert_object_ids
from ..images.service import image_storage_service


router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"],
)
collection = "recipes"


@router.get("/recommendations", status_code=status.HTTP_200_OK)
async def get_recipe_recommendations(
        db: AsyncIOMotorClient = Depends(get_db),
        locked_ids: Optional[str] = Query(None, description="Comma-separated list of locked recipe IDs"),
        min_rating: Optional[float] = Query(4.0, description="Minimum recipe rating", ge=0.0, le=5.0),
        min_votes: Optional[int] = Query(100, description="Minimum number of votes", ge=0),
        max_votes: Optional[int] = Query(None, description="Maximum number of votes", ge=0),
        has_image: Optional[bool] = Query(True, description="Only recipes with images"),
        tag_ids: Optional[str] = Query(None, description="Comma-separated list of tag IDs"),
        difficulty: Optional[str] = Query(None, description="Comma-separated difficulty levels (1,2,3)"),
        min_cooking_time: Optional[int] = Query(None, description="Minimum cooking time in minutes", ge=0),
        max_cooking_time: Optional[int] = Query(None, description="Maximum cooking time in minutes", ge=0),
        min_prep_time: Optional[int] = Query(None, description="Minimum preparation time in minutes", ge=0),
        max_prep_time: Optional[int] = Query(None, description="Maximum preparation time in minutes", ge=0),
        min_total_time: Optional[int] = Query(None, description="Minimum total time in minutes", ge=0),
        max_total_time: Optional[int] = Query(None, description="Maximum total time in minutes", ge=0)
) -> Dict[str, Any]:
    """
    Get 8 random recipe recommendations with customizable filters.
    Locked recipes will be kept in their positions and new random recipes will fill remaining slots.
    
    :param db: Database connection
    :param locked_ids: Comma-separated string of recipe IDs to keep locked in place
    :param min_rating: Minimum recipe rating (default: 4.0)
    :param min_votes: Minimum number of votes (default: 100)
    :param max_votes: Maximum number of votes
    :param has_image: Only include recipes with images (default: True)
    :param tag_ids: Comma-separated list of tag IDs to filter by
    :param difficulty: Comma-separated difficulty levels (1,2,3)
    :param min_cooking_time: Minimum cooking time in minutes
    :param max_cooking_time: Maximum cooking time in minutes
    :param min_prep_time: Minimum preparation time in minutes
    :param max_prep_time: Maximum preparation time in minutes
    :param min_total_time: Minimum total time in minutes
    :param max_total_time: Maximum total time in minutes
    :returns: Dictionary containing filtered recommended recipes
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
            # Build filter query based on parameters
            filter_query = {}
            
            # Exclude already locked recipes
            exclude_ids = [ObjectId(id) for id in locked_recipe_ids if ObjectId.is_valid(id)]
            if exclude_ids:
                filter_query["_id"] = {"$nin": exclude_ids}
            
            # Rating filter (handle null ratings)
            if min_rating is not None and min_rating > 0:
                # Only apply rating filter if min_rating is above 0
                # This allows null ratings to pass through when min_rating is 0
                filter_query["rating"] = {"$gte": min_rating}
            
            # Votes filter (using sourceRatingVotes, handle null values)
            if min_votes is not None and min_votes > 0:
                # Only apply votes filter if min_votes is above 0
                filter_query["sourceRatingVotes"] = {"$gte": min_votes}
            if max_votes is not None:
                if "sourceRatingVotes" in filter_query:
                    filter_query["sourceRatingVotes"]["$lte"] = max_votes
                else:
                    filter_query["sourceRatingVotes"] = {"$lte": max_votes}
            
            # Image filter
            if has_image:
                filter_query["previewImageUrlTemplate"] = {"$exists": True, "$ne": "", "$ne": None}
            
            # Tags filter
            if tag_ids:
                tag_id_list = [id.strip() for id in tag_ids.split(",") if id.strip()]
                valid_tag_ids = [ObjectId(id) for id in tag_id_list if ObjectId.is_valid(id)]
                if valid_tag_ids:
                    filter_query["tags"] = {"$in": valid_tag_ids}
            
            # Difficulty filter
            if difficulty:
                diff_levels = [int(d.strip()) for d in difficulty.split(",") if d.strip().isdigit() and 1 <= int(d.strip()) <= 3]
                if diff_levels:
                    filter_query["difficulty"] = {"$in": diff_levels}
            
            # Time filters
            if min_cooking_time is not None or max_cooking_time is not None:
                cooking_time_filter = {}
                if min_cooking_time is not None:
                    cooking_time_filter["$gte"] = min_cooking_time
                if max_cooking_time is not None:
                    cooking_time_filter["$lte"] = max_cooking_time
                filter_query["cookingTime"] = cooking_time_filter
            
            if min_prep_time is not None or max_prep_time is not None:
                prep_time_filter = {}
                if min_prep_time is not None:
                    prep_time_filter["$gte"] = min_prep_time
                if max_prep_time is not None:
                    prep_time_filter["$lte"] = max_prep_time
                filter_query["preparationTime"] = prep_time_filter
            
            if min_total_time is not None or max_total_time is not None:
                total_time_filter = {}
                if min_total_time is not None:
                    total_time_filter["$gte"] = min_total_time
                if max_total_time is not None:
                    total_time_filter["$lte"] = max_total_time
                filter_query["totalTime"] = total_time_filter
            
            # Build aggregation pipeline
            pipeline = []
            if filter_query:
                pipeline.append({"$match": filter_query})
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
            
            # Store image permanently if image URL template exists
            if recipe.previewImageUrlTemplate:
                try:
                    image_data = await image_storage_service.store_image(
                        recipe_id, recipe.previewImageUrlTemplate
                    )
                    
                    # Update recipe with stored image info
                    await db[collection].update_one(
                        {"_id": ObjectId(recipe_id)},
                        {"$set": image_data}
                    )
                except Exception as e:
                    # Log error but don't fail recipe creation
                    print(f"Failed to store image for recipe {recipe_id}: {str(e)}")
            
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
    
    # Store image if it exists but isn't stored yet
    if (recipe.get("previewImageUrlTemplate") and 
        not recipe.get("stored_image_url")):
        try:
            image_data = await image_storage_service.store_image(
                recipe_id, recipe["previewImageUrlTemplate"]
            )
            
            # Update recipe with stored image info
            await db[collection].update_one(
                {"_id": ObjectId(recipe_id)},
                {"$set": image_data}
            )
            
            # Update the recipe dict with stored image info
            recipe.update(image_data)
        except Exception as e:
            # Log error but don't fail recipe retrieval
            print(f"Failed to store image for recipe {recipe_id}: {str(e)}")
    
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
