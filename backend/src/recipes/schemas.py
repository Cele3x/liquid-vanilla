def serialize_recipe(recipe) -> dict:
    return {
        "id": str(recipe.get("_id")),
        "title": recipe.get("title")
    }


def serialize_recipes(recipes) -> list:
    return [serialize_recipe(recipe) for recipe in recipes]
