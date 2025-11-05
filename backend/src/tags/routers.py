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
async def get_tags(
    essential_only: bool = False,
    db: AsyncIOMotorClient = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Retrieve all tags or only essential tags.

    @param essential_only: If True, return only essential tags
    @param db: Database connection
    @return: List of tags
    """
    query = {"isEssential": True} if essential_only else {}
    tags = await db[collection].find(query).sort({ "usageCount": -1 }).to_list(None)
    return serialize_tags(tags)

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
