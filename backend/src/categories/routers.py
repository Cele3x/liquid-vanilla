from datetime import datetime
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from ..database import get_db
from .schemas import serialize_categories, serialize_category
from .models import Category

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)
collection = "categories"


@router.get("/", status_code=status.HTTP_200_OK)
async def get_categories(db: AsyncIOMotorClient = Depends(get_db)) -> List[Dict[str, Any]]:
    """
    Retrieve all categories ordered by name.

    :param db: Database connection
    :return: List of categories
    """
    categories = await db[collection].find().sort("name", 1).to_list(None)
    return serialize_categories(categories)


@router.get("/{category_id}", status_code=status.HTTP_200_OK)
async def get_category(category_id: str, db: AsyncIOMotorClient = Depends(get_db)) -> Dict[str, Any]:
    """
    Retrieve a specific category by ID.

    :param category_id: Category ID to retrieve
    :param db: Database connection
    :return: Category details
    :raises HTTPException: If category not found
    """
    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ungültiges Kategorie-ID-Format"
        )
    
    category = await db[collection].find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kategorie nicht gefunden"
        )
    
    return serialize_category(category)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(category: Category, db: AsyncIOMotorClient = Depends(get_db)) -> str:
    """
    Create a new category.

    :param category: Category model to create
    :param db: Database connection
    :return: Created category ID
    :raises HTTPException: If category creation fails
    """
    try:
        # Check if category with same name already exists
        existing_category = await db[collection].find_one({"name": category.name})
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Kategorie mit diesem Namen existiert bereits"
            )

        category_dict = category.model_dump()
        category_dict["createdAt"] = datetime.utcnow()
        category_dict["updatedAt"] = datetime.utcnow()
        
        result = await db[collection].insert_one(category_dict)

        if result.inserted_id:
            return str(result.inserted_id)

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Kategorie-Erstellung fehlgeschlagen"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{category_id}", status_code=status.HTTP_200_OK)
async def update_category(
    category_id: str, 
    category: Category, 
    db: AsyncIOMotorClient = Depends(get_db)
) -> Dict[str, Any]:
    """
    Update an existing category.

    :param category_id: Category ID to update
    :param category: Updated category data
    :param db: Database connection
    :return: Updated category
    :raises HTTPException: If category not found or update fails
    """
    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ungültiges Kategorie-ID-Format"
        )

    # Check if category exists
    existing_category = await db[collection].find_one({"_id": ObjectId(category_id)})
    if not existing_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kategorie nicht gefunden"
        )

    # Check if another category with the same name exists
    name_conflict = await db[collection].find_one({
        "name": category.name,
        "_id": {"$ne": ObjectId(category_id)}
    })
    if name_conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this name already exists"
        )

    category_dict = category.model_dump(exclude={"id"})
    category_dict["updatedAt"] = datetime.utcnow()

    result = await db[collection].update_one(
        {"_id": ObjectId(category_id)},
        {"$set": category_dict}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Kategorie-Update fehlgeschlagen"
        )

    updated_category = await db[collection].find_one({"_id": ObjectId(category_id)})
    return serialize_category(updated_category)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: str, db: AsyncIOMotorClient = Depends(get_db)) -> None:
    """
    Delete a category.

    :param category_id: Category ID to delete
    :param db: Database connection
    :raises HTTPException: If category not found or has associated tags
    """
    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ungültiges Kategorie-ID-Format"
        )

    # Check if category exists
    category = await db[collection].find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kategorie nicht gefunden"
        )

    # Check if any tags are using this category
    tags_using_category = await db["tags"].find_one({"categoryId": category_id})
    if tags_using_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Kategorie kann nicht gelöscht werden, da sie verknüpfte Tags hat"
        )

    result = await db[collection].delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Kategorie-Löschung fehlgeschlagen"
        )