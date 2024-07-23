def serialize_recipe(recipe) -> dict:
    return {
        "id": str(recipe.get("_id")),
        "name": recipe.get("name"),
        "description": recipe.get("description")
    }


def serialize_recipes(recipes) -> list:
    return [serialize_recipe(recipe) for recipe in recipes]
