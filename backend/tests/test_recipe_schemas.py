"""
Tests for recipe serialization schemas.

:module: tests.test_recipe_schemas
"""
from datetime import datetime, UTC

from src.recipes.schemas import serialize_recipe


class TestRecipeSchemas:
    """Test suite for Recipe serialization schemas."""

    def test_serialize_recipe_preserves_other_fields(self):
        """Test that serialization emits exactly the expected field set."""
        recipe_data = {
            "_id": "507f1f77bcf86cd799439011",
            "title": "Complete Test Recipe",
            "rating": 4.5,
            "sourceUrl": "https://example.com/recipes/test",
            "previewImageUrlTemplate": "https://example.com/images/<format>/test.jpg",
            "additionalDescription": "A complete test recipe",
            "preparationTime": 15,
            "restingTime": 5,
            "source": "Test Source",
            "sourceId": "test123",
            "status": "active",
            "cookingTime": 30,
            "servings": 4,
            "sourceRating": 4.7,
            "subtitle": "Complete test",
            "createdAt": datetime.now(UTC).isoformat(),
            "sourceRatingVotes": 100,
            "tagIds": ["tag1", "tag2"],
            "difficulty": 2,
            "sourceViewCount": 1000,
            "totalTime": 50,
            "userId": "user123",
            "ingredientsText": "Test ingredients",
            "instructions": "Test instructions",
            "miscellaneousText": "Test notes"
        }

        serialized = serialize_recipe(recipe_data)

        # Verify all fields are preserved
        expected_fields = {
            "id", "title", "rating", "score", "sourceUrl", "previewImageUrlTemplate",
            "additionalDescription", "preparationTime", "restingTime", "source",
            "sourceId", "status", "cookingTime", "servings", "sourceRating",
            "subtitle", "createdAt", "sourceRatingVotes", "tagIds", "difficulty",
            "sourceViewCount", "totalTime", "userId", "ingredientsText",
            "instructions", "miscellaneousText", "ingredientGroups"
        }

        assert set(serialized.keys()) == expected_fields
        assert serialized["id"] == "507f1f77bcf86cd799439011"
        assert serialized["previewImageUrlTemplate"] == "https://example.com/images/<format>/test.jpg"
