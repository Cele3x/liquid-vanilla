from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from ..database import get_db
from .schemas import serialize_tags
from .models import Tag

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)
collection = "tags"

@router.get("/", status_code=status.HTTP_200_OK)
async def get_tags(db: AsyncIOMotorClient = Depends(get_db)) -> List[Dict[str, Any]]:
    """
    Retrieve all tags with smart ordering and real usage counts.

    @param db: Database connection
    @return: List of tags ordered by logical groups with calculated usage counts
    """
    tags = await db[collection].find().to_list(None)
    
    # Calculate real usage counts by counting recipes that use each tag
    recipes_collection = db["recipes"]
    
    # Get all recipes and count tag usage
    recipes = await recipes_collection.find({}, {"tags": 1}).to_list(None)
    tag_usage_count = {}
    
    for recipe in recipes:
        tag_ids = recipe.get("tags", [])
        if tag_ids:
            for tag_id in tag_ids:
                tag_id_str = str(tag_id)
                tag_usage_count[tag_id_str] = tag_usage_count.get(tag_id_str, 0) + 1
    
    # Update tags with real usage counts
    for tag in tags:
        tag_id_str = str(tag.get("_id"))
        tag["usage_count"] = tag_usage_count.get(tag_id_str, 0)
    
    # Invalid tags to put at bottom
    invalid_tags = {'oder', 'klare', 'klar', 'öl', 'Essig', 'gewürze', 'lateinamerika'}
    
    # Fallback priority groups for tags without categoryId
    priority_groups = {
        'Hauptspeise': (100, 0), 'Vorspeise': (100, 1), 'Beilage': (100, 2), 'Snack': (100, 3), 
        'Dessert': (100, 4), 'Süßspeise': (100, 5), 'Frühstück': (100, 6),
        
        'Vegetarisch': (200, 0), 'Vegan': (200, 1), 'Low Carb': (200, 2), 'ketogen': (200, 3),
        
        'Backen': (300, 0), 'Braten': (300, 1), 'Grillen': (300, 2), 'Dünsten': (300, 3),
        
        'Fleisch': (400, 0), 'Fisch': (400, 1), 'Gemüse': (400, 2), 'Reis': (400, 3), 
        'Pasta': (400, 4), 'Nudeln': (400, 5), 'Kartoffeln': (400, 6),
        
        'Suppe': (500, 0), 'Salat': (500, 1), 'Eintopf': (500, 2), 'Pizza': (500, 3),
        
        'Deutschland': (600, 0), 'Italien': (600, 1), 'China': (600, 2), 'Japan': (600, 3),
        
        'Sommer': (700, 0), 'Winter': (700, 1), 'Weihnachten': (700, 2), 'Ostern': (700, 3),
        
        'Getränk': (800, 0), 'Cocktail': (800, 1), 'Kaffee Tee oder Kakao': (800, 2)
    }
    
    def get_sort_key(tag):
        tag_name = tag.get('name', '').strip()
        
        # Invalid tags go to bottom
        if tag_name in invalid_tags:
            return (9999, tag_name)
        
        # Use predefined priority if available
        if tag_name in priority_groups:
            return priority_groups[tag_name]
        
        # Default: alphabetical within middle range
        return (5000, tag_name.lower())
    
    # Sort and return
    sorted_tags = sorted(tags, key=get_sort_key)
    return serialize_tags(sorted_tags)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tag(tag: Tag, db: AsyncIOMotorClient = Depends(get_db)) -> str:
    """
    Create a new tag.

    @param tag: Tag model to create
    @param db: Database connection
    @return: Created tag ID
    @raise HTTPException: If tag creation fails
    """
    try:
        tag_dict = tag.model_dump()
        result = await db[collection].insert_one(tag_dict)

        if result.inserted_id:
            return str(result.inserted_id)

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Tag creation failed"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
