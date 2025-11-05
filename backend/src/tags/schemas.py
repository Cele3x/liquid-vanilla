
def serialize_tags(tags: list) -> list:
    return [
        {
            "id": str(tag.get("_id")), 
            "name": tag.get("name"),
            "categoryId": str(tag.get("categoryId")) if tag.get("categoryId") else None,
            "usageCount": tag.get("usageCount", 0)
        } 
        for tag in tags
    ]
