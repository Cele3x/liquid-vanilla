"""
Tests for updated recipe schemas with cached image fields.

:module: tests.test_recipe_schemas
"""
import pytest
from datetime import datetime, UTC

from src.recipes.schemas import serialize_recipe, serialize_recipes


class TestRecipeSchemas:
    """Test suite for Recipe serialization schemas with cached image fields."""

    def test_serialize_recipe_with_cached_image_fields(self):
        """Test recipe serialization with cached image fields."""
        recipe_data = {
            "_id": "507f1f77bcf86cd799439011",
            "title": "Test Recipe",
            "rating": 4.5,
            "previewImageUrlTemplate": "https://example.com/images/<format>/test.jpg",
            "cachedImagePath": "/cache/path/test_image.jpg", 
            "cachedImageUrl": "/api/v1/images/test_image.jpg",
            "imageCachedAt": datetime.now(UTC).isoformat(),
            "sourceUrl": "https://example.com/recipes/test",
            "additionalDescription": "Test description",
            "instructions": "Test instructions",
            "ingredientsText": "Test ingredients"
        }
        
        serialized = serialize_recipe(recipe_data)
        
        assert serialized["id"] == "507f1f77bcf86cd799439011"
        assert serialized["title"] == "Test Recipe"
        assert serialized["cachedImagePath"] == "/cache/path/test_image.jpg"
        assert serialized["cachedImageUrl"] == "/api/v1/images/test_image.jpg"
        assert serialized["imageCachedAt"] == recipe_data["imageCachedAt"]

    def test_serialize_recipe_without_cached_image_fields(self):
        """Test recipe serialization without cached image fields."""
        recipe_data = {
            "_id": "507f1f77bcf86cd799439011",
            "title": "Test Recipe",
            "rating": 4.5,
            "instructions": "Test instructions",
            "ingredientsText": "Test ingredients"
        }
        
        serialized = serialize_recipe(recipe_data)
        
        assert serialized["id"] == "507f1f77bcf86cd799439011"
        assert serialized["title"] == "Test Recipe"
        assert serialized["cachedImagePath"] is None
        assert serialized["cachedImageUrl"] is None
        assert serialized["imageCachedAt"] is None

    def test_serialize_recipe_with_none_cached_fields(self):
        """Test recipe serialization with None cached image fields."""
        recipe_data = {
            "_id": "507f1f77bcf86cd799439011", 
            "title": "Test Recipe",
            "rating": 4.5,
            "cachedImagePath": None,
            "cachedImageUrl": None,
            "imageCachedAt": None,
            "instructions": "Test instructions",
            "ingredientsText": "Test ingredients"
        }
        
        serialized = serialize_recipe(recipe_data)
        
        assert serialized["id"] == "507f1f77bcf86cd799439011"
        assert serialized["title"] == "Test Recipe"
        assert serialized["cachedImagePath"] is None
        assert serialized["cachedImageUrl"] is None
        assert serialized["imageCachedAt"] is None

    def test_serialize_recipes_with_mixed_cached_fields(self):
        """Test serializing multiple recipes with mixed cached image fields."""
        recipes_data = [
            {
                "_id": "507f1f77bcf86cd799439011",
                "title": "Recipe with Cached Image",
                "cachedImageUrl": "/api/v1/images/cached.jpg",
                "instructions": "Test instructions",
                "ingredientsText": "Test ingredients"
            },
            {
                "_id": "507f1f77bcf86cd799439012", 
                "title": "Recipe without Cached Image",
                "instructions": "Test instructions",
                "ingredientsText": "Test ingredients"
            }
        ]
        
        serialized = serialize_recipes(recipes_data)
        
        assert len(serialized) == 2
        assert serialized[0]["cachedImageUrl"] == "/api/v1/images/cached.jpg"
        assert serialized[1]["cachedImageUrl"] is None

    def test_serialize_recipe_preserves_other_fields(self):
        """Test that serialization preserves all other existing fields."""
        recipe_data = {
            "_id": "507f1f77bcf86cd799439011",
            "title": "Complete Test Recipe",
            "rating": 4.5,
            "sourceUrl": "https://example.com/recipes/test",
            "previewImageUrlTemplate": "https://example.com/images/<format>/test.jpg",
            "cachedImagePath": "/cache/path/test_image.jpg",
            "cachedImageUrl": "/api/v1/images/test_image.jpg", 
            "imageCachedAt": datetime.now(UTC).isoformat(),
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
            "id", "title", "rating", "sourceUrl", "previewImageUrlTemplate",
            "cachedImagePath", "cachedImageUrl", "imageCachedAt",
            "additionalDescription", "preparationTime", "restingTime", "source",
            "sourceId", "status", "cookingTime", "servings", "sourceRating",
            "subtitle", "createdAt", "sourceRatingVotes", "tagIds", "difficulty",
            "sourceViewCount", "totalTime", "userId", "ingredientsText",
            "instructions", "miscellaneousText", "ingredientGroups"
        }
        
        assert set(serialized.keys()) == expected_fields
        assert serialized["id"] == "507f1f77bcf86cd799439011"
        assert serialized["cachedImagePath"] == "/cache/path/test_image.jpg"
        assert serialized["cachedImageUrl"] == "/api/v1/images/test_image.jpg"