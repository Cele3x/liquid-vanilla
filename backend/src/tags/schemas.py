
def serialize_tags(tags: list) -> list:
    return [{
        "id": str(tag.get("_id")), 
        "name": tag.get("name"), 
        "usage_count": tag.get("usage_count", 0),
        "categoryId": str(tag.get("categoryId")) if tag.get("categoryId") else None
    } for tag in tags]
