from typing import List
from .models import Category


def serialize_category(category: dict) -> dict:
    """
    Serialize category data for API response.
    
    :param category: Category document from database
    :returns: Serialized category data
    """
    return {
        "id": str(category["_id"]),
        "name": category["name"],
        "description": category.get("description"),
        "order": category.get("order", 0)
    }


def serialize_categories(categories: List[dict]) -> List[dict]:
    """
    Serialize multiple categories for API response.
    
    :param categories: List of category documents from database
    :returns: List of serialized category data
    """
    return [serialize_category(category) for category in categories]