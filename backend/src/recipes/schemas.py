def serialize_tags(tag_ids: list) -> list:
    if not tag_ids:
        return []
    return [str(tag_id) for tag_id in tag_ids if tag_ids]


def serialize_ingredient(ingredient: dict) -> dict:
    return {
        "ingredientId": str(ingredient.get("ingredientId")),
        "unitId": str(ingredient.get("unitId")),
        "amount": ingredient.get("amount")
    }


def serialize_ingredients(ingredients: list) -> list:
    if not ingredients:
        return []
    return [serialize_ingredient(ingredient) for ingredient in ingredients]


def serialize_ingredient_group(ingredient_group: dict) -> dict:
    return {
        "header": ingredient_group.get("header"),
        "ingredients": serialize_ingredients(ingredient_group.get("ingredients"))
    }


def serialize_ingredient_groups(ingredient_groups: list) -> list:
    if not ingredient_groups:
        return []
    return [serialize_ingredient_group(ingredient_group) for ingredient_group in ingredient_groups]


def serialize_recipe(recipe: dict) -> dict:
    return {
        "id": str(recipe.get("_id")),
        "title": recipe.get("title"),
        "rating": recipe.get("rating"),
        "previewImageUrlTemplate": recipe.get("previewImageUrlTemplate"),
        "cachedImagePath": recipe.get("cachedImagePath"),
        "cachedImageUrl": recipe.get("cachedImageUrl"),
        "imageCachedAt": recipe.get("imageCachedAt"),
        "sourceUrl": recipe.get("sourceUrl"),
        "additionalDescription": recipe.get("additionalDescription"),
        "preparationTime": recipe.get("preparationTime"),
        "restingTime": recipe.get("restingTime"),
        "source": recipe.get("source"),
        "sourceId": recipe.get("sourceId"),
        "status": recipe.get("status"),
        "cookingTime": recipe.get("cookingTime"),
        "servings": recipe.get("servings"),
        "sourceRating": recipe.get("sourceRating"),
        "subtitle": recipe.get("subtitle"),
        "createdAt": recipe.get("createdAt"),
        "sourceRatingVotes": recipe.get("sourceRatingVotes"),
        "tagIds": serialize_tags(recipe.get("tagIds")),
        "ingredientGroups": serialize_ingredient_groups(recipe.get("ingredientGroups")),
        "difficulty": recipe.get("difficulty"),
        "sourceViewCount": recipe.get("sourceViewCount"),
        "totalTime": recipe.get("totalTime"),
        "userId": str(recipe.get("userId")),
        "ingredientsText": recipe.get("ingredientsText"),
        "instructions": recipe.get("instructions"),
        "miscellaneousText": recipe.get("miscellaneousText")
    }


def serialize_recipes(recipes: list) -> list:
    return [serialize_recipe(recipe) for recipe in recipes]
