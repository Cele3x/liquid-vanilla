def serialize_recipe(recipe) -> dict:
    return {
        "id": str(recipe.get("_id")),
        "title": recipe.get("title"),
        "rating": recipe.get("rating"),
        "previewImageUrlTemplate": recipe.get("previewImageUrlTemplate"),
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
        "tags": recipe.get("tags"),
        "difficulty": recipe.get("difficulty"),
        "sourceViewCount": recipe.get("sourceViewCount"),
        "totalTime": recipe.get("totalTime"),
        "userId": recipe.get("userId"),
        "ingredientsText": recipe.get("ingredientsText"),
        "instructions": recipe.get("instructions"),
        "miscellaneousText": recipe.get("miscellaneousText")
    }


def serialize_recipes(recipes) -> list:
    return [serialize_recipe(recipe) for recipe in recipes]
