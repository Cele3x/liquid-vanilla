"""
Integration tests for recipe and image storage functionality.

:module: tests.test_recipe_image_integration
"""
import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime, UTC

from src.config import settings

RECIPE_URL = f"{settings.BASE_URL}/recipes"


class TestRecipeImageIntegration:
    """Test suite for Recipe and Image integration."""

    @pytest.fixture
    def recipe_with_image(self):
        """Recipe fixture with image URL template."""
        return {
            "title": "Recipe with Image",
            "rating": 4.5,
            "previewImageUrlTemplate": "https://example.com/images/<format>/recipe.jpg",
            "additionalDescription": "Recipe for testing image storage",
            "instructions": "Step 1: Test\nStep 2: Verify",
            "ingredientsText": "Test ingredient",
        }

    def test_create_recipe_stores_image(self, client, recipe_with_image, mock_image_storage_service):
        """Test that creating a recipe triggers image storage."""
        response = client.post(RECIPE_URL, json=recipe_with_image)
        
        assert response.status_code == 201
        recipe_id = response.json()
        
        # Verify image storage was called
        mock_image_storage_service.store_image.assert_called_once_with(
            recipe_id, recipe_with_image["previewImageUrlTemplate"]
        )

    def test_create_recipe_without_image_no_storage(self, client, mock_image_storage_service):
        """Test that creating a recipe without image doesn't trigger storage."""
        recipe_without_image = {
            "title": "Recipe without Image",
            "instructions": "Step 1: Test",
            "ingredientsText": "Test ingredient",
        }
        
        response = client.post(RECIPE_URL, json=recipe_without_image)
        
        assert response.status_code == 201
        
        # Verify image caching was not called
        mock_image_storage_service.store_image.assert_not_called()

    def test_get_recipe_behavior(self, client, recipe_with_image, mock_image_cache_service):
        """Test recipe retrieval behavior."""
        # Create recipe first
        create_response = client.post(RECIPE_URL, json=recipe_with_image)
        recipe_id = create_response.json()
        
        response = client.get(f"{RECIPE_URL}/{recipe_id}")
        
        assert response.status_code == 200
        recipe_data = response.json()
        assert recipe_data["id"] == recipe_id

    def test_image_storage_failure_doesnt_break_recipe_creation(self, client, recipe_with_image):
        """Test that image storage failure doesn't prevent recipe creation."""
        with patch('src.recipes.routers.image_storage_service.store_image') as mock_storage:
            mock_storage.side_effect = Exception("Network error")
            
            response = client.post(RECIPE_URL, json=recipe_with_image)
            
            assert response.status_code == 201
            recipe_id = response.json()
            assert recipe_id is not None

    def test_image_storage_failure_doesnt_break_recipe_retrieval(self, client, recipe_with_image):
        """Test that image storage failure doesn't prevent recipe retrieval."""
        # Create recipe first
        create_response = client.post(RECIPE_URL, json=recipe_with_image)
        recipe_id = create_response.json()
        
        with patch('src.recipes.routers.image_storage_service.store_image') as mock_storage:
            mock_storage.side_effect = Exception("Network error")
            
            response = client.get(f"{RECIPE_URL}/{recipe_id}")
            
            assert response.status_code == 200
            recipe_data = response.json()
            assert recipe_data["id"] == recipe_id

    def test_recipe_response_includes_stored_image_fields(self, client, recipe_with_image):
        """Test that recipe response includes stored image fields."""
        # Create recipe first
        create_response = client.post(RECIPE_URL, json=recipe_with_image)
        recipe_id = create_response.json()
        
        response = client.get(f"{RECIPE_URL}/{recipe_id}")
        
        assert response.status_code == 200
        recipe_data = response.json()
        
        # Verify cached image fields are present (they might be None)
        assert "cachedImagePath" in recipe_data
        assert "cachedImageUrl" in recipe_data  
        assert "imageCachedAt" in recipe_data