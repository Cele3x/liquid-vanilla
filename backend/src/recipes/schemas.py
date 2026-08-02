from typing import Any, Optional


def serialize_tags(tag_ids: list) -> list:
    if not tag_ids:
        return []
    return [str(tag_id) for tag_id in tag_ids if tag_ids]


def serialize_rating(rating: Any) -> Optional[float]:
    """
    Normalize a stored rating to a plain float.

    Accepts both the embedded document ``{"rating": float, "numVotes": int}`` and the
    flat float legacy documents carry. Values that are not usable numbers yield ``None``.

    :param rating: Raw rating value as stored in the database
    :returns: The rating as a float, or None if the value is unusable
    """
    if isinstance(rating, dict):
        rating = rating.get("rating")
    if isinstance(rating, bool) or not isinstance(rating, (int, float)):
        return None
    return float(rating)


def serialize_display_rating(recipe: dict) -> Optional[float]:
    """
    Resolve the star average shown to the user.

    ``sourceRating`` holds the untouched average the source's own users gave, which is
    the only rating meant for display. Legacy documents predating the split store a
    computed value in a flat ``rating`` and have no ``sourceRating``; those fall back to
    it so their cards keep rendering stars.

    :param recipe: Raw recipe document from the database
    :returns: The star average as a float, or None if the recipe has no rating
    """
    rating = recipe.get("sourceRating")
    if isinstance(rating, bool) or not isinstance(rating, (int, float)):
        return serialize_rating(recipe.get("rating"))
    return float(rating)


def serialize_score(recipe: dict) -> Optional[float]:
    """
    Resolve the normalized score a recipe is ordered by.

    ``rating.rating`` holds a 0-5 score expressing where a recipe ranks inside its own
    source, so recipes from sites that grade differently can share one sorted list. It
    is never displayed. A flat ``rating`` predates the split and carries no score.

    :param recipe: Raw recipe document from the database
    :returns: The score as a float, or None if the recipe was never scored
    """
    rating = recipe.get("rating")
    if not isinstance(rating, dict):
        return None
    return serialize_rating(rating)


def serialize_rating_votes(recipe: dict) -> Optional[int]:
    """
    Resolve the number of votes backing a recipe rating.

    Prefers the flat ``sourceRatingVotes`` field and falls back to the ``numVotes``
    entry of the embedded rating document.

    :param recipe: Raw recipe document from the database
    :returns: Vote count as an int, or None if unavailable
    """
    votes = recipe.get("sourceRatingVotes")
    if votes is None:
        rating = recipe.get("rating")
        if isinstance(rating, dict):
            votes = rating.get("numVotes")
    if isinstance(votes, bool) or not isinstance(votes, (int, float)):
        return None
    return int(votes)


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
        "rating": serialize_display_rating(recipe),
        "score": serialize_score(recipe),
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
        "sourceRatingVotes": serialize_rating_votes(recipe),
        "tagIds": serialize_tags(recipe.get("tagIds") or recipe.get("tags")),
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
