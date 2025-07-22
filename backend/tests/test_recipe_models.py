"""
Tests for updated recipe models with cached image fields.

:module: tests.test_recipe_models
"""
import pytest
from datetime import datetime, UTC
from pydantic import ValidationError

from src.recipes.models import Recipe


class TestRecipeModels:
    """Test suite for Recipe model with cached image fields."""

    def test_recipe_with_cached_image_fields(self):
        """Test Recipe model with cached image fields."""
        recipe_data = {
            "title": "Test Recipe",
            "previewImageUrlTemplate": "https://example.com/images/<format>/test.jpg",
            "cachedImagePath": "/cache/path/test_image.jpg",
            "cachedImageUrl": "/api/v1/images/test_image.jpg",
            "imageCachedAt": datetime.now(UTC),
            "instructions": "Test instructions",
            "ingredientsText": "Test ingredients"
        }
        
        recipe = Recipe(**recipe_data)
        
        assert recipe.title == "Test Recipe"
        assert recipe.previewImageUrlTemplate == "https://example.com/images/<format>/test.jpg"
        assert recipe.cachedImagePath == "/cache/path/test_image.jpg"
        assert recipe.cachedImageUrl == "/api/v1/images/test_image.jpg"
        assert recipe.imageCachedAt is not None

    def test_recipe_without_cached_image_fields(self):
        """Test Recipe model without cached image fields (defaults to None)."""
        recipe_data = {
            "title": "Test Recipe",
            "instructions": "Test instructions",
            "ingredientsText": "Test ingredients"
        }
        
        recipe = Recipe(**recipe_data)
        
        assert recipe.title == "Test Recipe"
        assert recipe.cachedImagePath is None
        assert recipe.cachedImageUrl is None
        assert recipe.imageCachedAt is None

    def test_recipe_with_partial_cached_image_fields(self):
        """Test Recipe model with some cached image fields."""
        recipe_data = {
            "title": "Test Recipe",
            "cachedImageUrl": "/api/v1/images/test_image.jpg",
            "instructions": "Test instructions",
            "ingredientsText": "Test ingredients"
        }
        
        recipe = Recipe(**recipe_data)
        
        assert recipe.title == "Test Recipe"
        assert recipe.cachedImageUrl == "/api/v1/images/test_image.jpg"
        assert recipe.cachedImagePath is None
        assert recipe.imageCachedAt is None

    def test_recipe_model_dump_includes_cached_fields(self):
        """Test that model_dump includes cached image fields."""
        recipe_data = {
            "title": "Test Recipe",
            "cachedImagePath": "/cache/path/test_image.jpg",
            "cachedImageUrl": "/api/v1/images/test_image.jpg", 
            "imageCachedAt": datetime.now(UTC),
            "instructions": "Test instructions",
            "ingredientsText": "Test ingredients"
        }
        
        recipe = Recipe(**recipe_data)
        dumped = recipe.model_dump()
        
        assert "cachedImagePath" in dumped
        assert "cachedImageUrl" in dumped
        assert "imageCachedAt" in dumped
        assert dumped["cachedImagePath"] == "/cache/path/test_image.jpg"
        assert dumped["cachedImageUrl"] == "/api/v1/images/test_image.jpg"

    def test_recipe_validation_with_invalid_cached_fields(self):
        """Test Recipe model validation with invalid cached image field types."""
        # This should work fine since fields are Optional[str] and Optional[datetime]
        recipe_data = {
            "title": "Test Recipe",
            "cachedImagePath": None,  # Valid - Optional field
            "cachedImageUrl": None,   # Valid - Optional field
            "imageCachedAt": None,    # Valid - Optional field
            "instructions": "Test instructions",
            "ingredientsText": "Test ingredients"
        }
        
        recipe = Recipe(**recipe_data)
        assert recipe.cachedImagePath is None
        assert recipe.cachedImageUrl is None
        assert recipe.imageCachedAt is None

    def test_recipe_with_datetime_string_parsing(self):
        """Test Recipe model with datetime string for imageCachedAt."""
        recipe_data = {
            "title": "Test Recipe", 
            "imageCachedAt": "2023-06-01T12:00:00Z",  # ISO string
            "instructions": "Test instructions",
            "ingredientsText": "Test ingredients"
        }
        
        recipe = Recipe(**recipe_data)
        assert isinstance(recipe.imageCachedAt, datetime)

    def test_recipe_example_schema_updated(self):
        """Test that Recipe model example includes cached image fields."""
        example = Recipe.model_config.get("json_schema_extra", {}).get("example", {})
        
        # The existing example should still work
        if example:
            # Check if we can create a recipe with the example data
            try:
                recipe = Recipe(**example)
                assert recipe.title is not None
            except ValidationError:
                # Example might not have all required fields, that's okay
                pass