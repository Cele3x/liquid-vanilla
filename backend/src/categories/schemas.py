def serialize_categories(categories: list) -> list:
    """
    Serialize categories from MongoDB documents to API response format.
    
    :param categories: List of category documents from MongoDB
    :return: List of serialized category objects
    """
    return [
        {
            "id": str(category.get("_id")),
            "name": category.get("name"),
            "description": category.get("description"),
            "createdAt": category.get("createdAt"),
            "updatedAt": category.get("updatedAt")
        }
        for category in categories
    ]


def serialize_category(category: dict) -> dict:
    """
    Serialize a single category from MongoDB document to API response format.
    
    :param category: Category document from MongoDB
    :return: Serialized category object
    """
    return {
        "id": str(category.get("_id")),
        "name": category.get("name"),
        "description": category.get("description"),
        "createdAt": category.get("createdAt"),
        "updatedAt": category.get("updatedAt")
    }