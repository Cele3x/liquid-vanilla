
def serialize_tags(tags: list) -> list:
    return [{"id": str(tag.get("_id")), "name": tag.get("name")} for tag in tags]
