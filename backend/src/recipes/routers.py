from itertools import zip_longest
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

# The normalized 0-5 score written by the scraper's rating pipeline, stored inside the
# embedded rating document. It expresses where a recipe ranks within its own source, so
# ordering it against another source is meaningful; the star average users see lives in
# "sourceRating" and is never sorted on.
SCORE_FIELD = "rating.rating"

# Tag references live under "tags"; a few legacy documents use "tagIds" instead.
TAG_FIELDS = ("tags", "tagIds")

# Recommendation slots to fill per request.
RECOMMENDATION_SIZE = 8

# Fields holding ObjectId references that arrive from clients as strings.
OBJECT_ID_FIELDS = [
    "tags",
    "tagIds",
    "userId",
    "ingredientGroups.ingredients.ingredientId",
    "ingredientGroups.ingredients.unitId",
]


def prepare_recipe_document(recipe: Recipe) -> Dict[str, Any]:
    """
    Turn an incoming recipe into the document shape used by the collection.

    ObjectId references are converted from their string form, and the rating the client
    supplies is stored as ``sourceRating`` - both name the same thing, the raw star
    average. An explicit ``sourceRating`` wins when a client sends both.

    The embedded ``rating`` document is deliberately not written: it holds the
    normalized score that only the scraper's rating pipeline can compute, and a client
    value placed there would order the recipe against a scale it was never measured on.

    :param recipe: Recipe model received from the client
    :returns: Document ready to be written to MongoDB
    """
    recipe_dict = convert_object_ids(recipe.model_dump(), OBJECT_ID_FIELDS)
    rating = recipe_dict.pop("rating", None)
    if recipe_dict.get("sourceRating") is None and isinstance(rating, (int, float)) \
            and not isinstance(rating, bool):
        recipe_dict["sourceRating"] = float(rating)
    return recipe_dict


def build_recommendation_filter(
        exclude_ids: List[ObjectId],
        min_score: Optional[float],
        min_votes: Optional[int],
        max_votes: Optional[int],
        has_image: Optional[bool],
        tag_ids: Optional[str],
        difficulty: Optional[str],
) -> Dict[str, Any]:
    """
    Build the MongoDB filter selecting the recipes a recommendation may be drawn from.

    :param exclude_ids: Recipe ids already held by locked slots
    :param min_score: Minimum normalized score, where 4.0 keeps the top 20% of a source
    :param min_votes: Minimum number of votes backing the star average
    :param max_votes: Maximum number of votes backing the star average
    :param has_image: Only include recipes carrying a preview image
    :param tag_ids: Comma-separated list of tag IDs to filter by
    :param difficulty: Comma-separated difficulty levels (1,2,3)
    :returns: Filter document, empty when nothing was restricted
    """
    filter_query: Dict[str, Any] = {}

    if exclude_ids:
        filter_query["_id"] = {"$nin": exclude_ids}

    # Recipes that were never scored have no score field and drop out here, which is
    # why the default is permissive rather than the top of the scale.
    if min_score is not None and min_score > 0:
        filter_query[SCORE_FIELD] = {"$gte": min_score}

    # Votes back the star average, so they are counted on the raw source field. Vote
    # weight is already folded into the score; this only exists to raise the floor.
    votes_filter: Dict[str, Any] = {}
    if min_votes is not None and min_votes > 0:
        votes_filter["$gte"] = min_votes
    if max_votes is not None:
        votes_filter["$lte"] = max_votes
    if votes_filter:
        filter_query["sourceRatingVotes"] = votes_filter

    if has_image:
        filter_query["previewImageUrlTemplate"] = {"$exists": True, "$nin": ["", None]}

    if tag_ids:
        tag_id_list = [tag_id.strip() for tag_id in tag_ids.split(",") if tag_id.strip()]
        valid_tag_ids = [ObjectId(tag_id) for tag_id in tag_id_list if ObjectId.is_valid(tag_id)]
        if valid_tag_ids:
            filter_query["$or"] = [{field: {"$in": valid_tag_ids}} for field in TAG_FIELDS]

    if difficulty:
        diff_levels = [
            int(level.strip()) for level in difficulty.split(",")
            if level.strip().isdigit() and 1 <= int(level.strip()) <= 3
        ]
        if diff_levels:
            filter_query["difficulty"] = {"$in": diff_levels}

    return filter_query


async def sample_recipes(db: AsyncIOMotorClient, filter_query: Dict[str, Any],
                         needed: int, sources: Optional[List[str]]) -> List[Dict[str, Any]]:
    """
    Draw random recipes, spread evenly over the sources that are in play.

    A single ``$sample`` over the whole collection returns recipes in proportion to how
    many each source contributes, so one site can take every slot of a page. Sampling
    each source separately and interleaving the results keeps the page mixed, and still
    fills every slot from the remaining sources when one of them runs short.

    :param db: Database connection
    :param filter_query: Filter selecting eligible recipes
    :param needed: Number of recipes to return
    :param sources: Sources to draw from, or None to use every source in the collection
    :returns: Sampled recipe documents, at most ``needed`` of them
    """
    if needed <= 0:
        return []

    candidates = sources
    if candidates is None:
        candidates = [source for source in await db[collection].distinct("source") if source]

    if len(candidates) <= 1:
        query = dict(filter_query)
        if candidates:
            query["source"] = candidates[0]
        pipeline = [{"$match": query}] if query else []
        pipeline.append({"$sample": {"size": needed}})
        return await db[collection].aggregate(pipeline).to_list(needed)

    # One branch per source, each sampled to the full page size so that a source with
    # too few matches can be covered by the others.
    facets = {
        f"source{index}": [
            {"$match": {**filter_query, "source": source}},
            {"$sample": {"size": needed}},
        ]
        for index, source in enumerate(candidates)
    }
    [grouped] = await db[collection].aggregate([{"$facet": facets}]).to_list(1)

    selected: List[Dict[str, Any]] = []
    for row in zip_longest(*(grouped.get(key, []) for key in facets)):
        for recipe in row:
            if recipe is None:
                continue
            selected.append(recipe)
            if len(selected) == needed:
                return selected
    return selected


@router.get("/recommendations", status_code=status.HTTP_200_OK)
async def get_recipe_recommendations(
        db: AsyncIOMotorClient = Depends(get_db),
        locked_ids: Optional[str] = Query(None, description="Comma-separated list of locked recipe IDs"),
        min_score: Optional[float] = Query(
            0.0,
            description="Minimum normalized score (0-5). 4.0 keeps the top 20% of every source",
            ge=0.0, le=5.0
        ),
        min_votes: Optional[int] = Query(0, description="Minimum number of votes", ge=0),
        max_votes: Optional[int] = Query(None, description="Maximum number of votes", ge=0),
        has_image: Optional[bool] = Query(True, description="Only recipes with images"),
        tag_ids: Optional[str] = Query(None, description="Comma-separated list of tag IDs"),
        difficulty: Optional[str] = Query(None, description="Comma-separated difficulty levels (1,2,3)"),
        sources: Optional[str] = Query(None, description="Comma-separated list of sources"),
) -> Dict[str, Any]:
    """
    Get 8 random recipe recommendations with customizable filters.
    Locked recipes will be kept in their positions and new random recipes will fill remaining slots.

    Recipes are drawn evenly from the sources in play rather than in proportion to how
    many recipes each source contributes.

    :param db: Database connection
    :param locked_ids: Comma-separated string of recipe IDs to keep locked in place
    :param min_score: Minimum normalized score, 0-5 (default: 0.0, no restriction)
    :param min_votes: Minimum number of votes (default: 0, no restriction)
    :param max_votes: Maximum number of votes
    :param has_image: Only include recipes with images (default: True)
    :param tag_ids: Comma-separated list of tag IDs to filter by
    :param difficulty: Comma-separated difficulty levels (1,2,3)
    :param sources: Comma-separated list of sources to draw from (default: all sources)
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
        needed_count = max(0, RECOMMENDATION_SIZE - len(locked_recipes))

        new_recipes = []
        if needed_count > 0:
            exclude_ids = [ObjectId(id) for id in locked_recipe_ids if ObjectId.is_valid(id)]
            filter_query = build_recommendation_filter(
                exclude_ids, min_score, min_votes, max_votes, has_image, tag_ids, difficulty
            )

            source_list = None
            if sources:
                source_list = [source.strip() for source in sources.split(",") if source.strip()]

            new_recipes = await sample_recipes(db, filter_query, needed_count, source_list)

        # Combine locked and new recipes
        all_recommendations = locked_recipes + new_recipes
        
        # Store images for recipes that have image URLs but no stored images
        for recipe in all_recommendations:
            if (recipe.get("previewImageUrlTemplate") and 
                not recipe.get("stored_image_url")):
                try:
                    recipe_id = str(recipe["_id"])
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
        
        return {
            "recommendations": serialize_recipes(all_recommendations)
        }
        
    except Exception as e:
        print(f"Aggregation failed, using fallback: {str(e)}")
        
        # Fallback - get first 8 recipes with images
        try:
            recommendations = await db[collection].find({
                "previewImageUrlTemplate": {"$exists": True, "$nin": ["", None]}
            }).limit(8).to_list(8)
            
            # Store images for fallback recipes that have image URLs but no stored images
            for recipe in recommendations:
                if (recipe.get("previewImageUrlTemplate") and 
                    not recipe.get("stored_image_url")):
                    try:
                        recipe_id = str(recipe["_id"])
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
            
            return {
                "recommendations": serialize_recipes(recommendations)
            }
        except:
            return {"recommendations": []}


@router.get("/sources", status_code=status.HTTP_200_OK)
async def get_recipe_sources(db: AsyncIOMotorClient = Depends(get_db)) -> Dict[str, Any]:
    """
    List the sites recipes have been collected from.

    Declared before the ``/{recipe_id}`` route so the path is not read as an id.

    :param db: Database connection
    :returns: Dictionary containing the sources, alphabetically
    """
    sources = [source for source in await db[collection].distinct("source") if source]
    return {"sources": sorted(sources)}


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
            query["$or"] = [{field: {"$in": tag_ids}} for field in TAG_FIELDS]
        except bson_errors.InvalidId as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid tag ID format: {str(e)}"
            )

    if search:
        query["title"] = {"$regex": search, "$options": "i"}

    # Large groups of recipes share one score exactly - tens of thousands of them carry
    # the same star average and vote count - so the score alone leaves their order
    # undefined and paging through such a group would repeat and skip recipes. The id
    # breaks those ties into a stable total order.
    sort_order = [(SCORE_FIELD, -1), ("_id", -1)]
    recipes = await db[collection].find(query).skip(skip).limit(page_size).sort(sort_order).to_list(page_size)
    total = await db[collection].count_documents(query)

    # Store images for recipes that have image URLs but no stored images
    for recipe in recipes:
        if (recipe.get("previewImageUrlTemplate") and 
            not recipe.get("stored_image_url")):
            try:
                recipe_id = str(recipe["_id"])
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
        converted_dict = prepare_recipe_document(recipe)
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
            detail="Rezept-Erstellung fehlgeschlagen"
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
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")
    
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
    result = await db[collection].find_one_and_update(
        {"_id": ObjectId(recipe_id)},
        {"$set": prepare_recipe_document(recipe)}
    )
    if not result:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")
    return recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(recipe_id: str, db: AsyncIOMotorClient = Depends(get_db)):
    result = await db[collection].find_one_and_delete({"_id": ObjectId(recipe_id)})
    if not result:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")
