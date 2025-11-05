from typing import List
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status

from .models import Category
from .schemas import serialize_categories
from ..database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)
collection = "categories"


@router.get("/", status_code=status.HTTP_200_OK)
async def get_categories(
        db: AsyncIOMotorClient = Depends(get_db),
) -> List[dict]:
    """
    Retrieve all categories sorted by order.

    :param db: Database connection
    :returns: List of serialized category data
    """
    categories = await db[collection].find().sort("order", 1).to_list(1000)
    return serialize_categories(categories)