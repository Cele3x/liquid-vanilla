def serialize_recipe(recipe) -> dict:
    return {
        "id": str(recipe.get("_id")),
        "title": recipe.get("title"),
        "rating": recipe.get("rating"),
        "previewImageUrlTemplate": recipe.get("previewImageUrlTemplate"),
    }


def serialize_recipes(recipes) -> list:
    return [serialize_recipe(recipe) for recipe in recipes]
