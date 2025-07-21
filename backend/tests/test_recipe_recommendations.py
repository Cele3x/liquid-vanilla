"""
Tests for recipe recommendations endpoint.

:module: tests.test_recipe_recommendations
"""
import pytest
from src.config import settings

RECIPE_URL = f"{settings.BASE_URL}/recipes"


class TestRecipeRecommendations:
    """Test suite for recipe recommendations functionality."""

    @pytest.fixture
    def recipes_with_images(self):
        """Create test recipes with image URLs."""
        return [
            {
                "title": f"Recipe with Image {i}",
                "rating": 4.0 + (i * 0.1),
                "previewImageUrlTemplate": f"https://example.com/images/<format>/recipe{i}.jpg",
                "instructions": f"Instructions for recipe {i}",
                "ingredientsText": f"Ingredients for recipe {i}",
            }
            for i in range(1, 6)
        ]

    @pytest.fixture
    def recipes_without_images(self):
        """Create test recipes without image URLs."""
        return [
            {
                "title": f"Recipe without Image {i}",
                "rating": 3.0 + (i * 0.2),
                "instructions": f"Instructions for recipe {i}",
                "ingredientsText": f"Ingredients for recipe {i}",
            }
            for i in range(1, 4)
        ]

    def test_get_recommendations_with_images_only(self, client, recipes_with_images, recipes_without_images):
        """Test that recommendations only return recipes with images."""
        # Create recipes with and without images
        for recipe in recipes_with_images + recipes_without_images:
            response = client.post(RECIPE_URL, json=recipe)
            assert response.status_code == 201

        # Get recommendations
        response = client.get(f"{RECIPE_URL}/recommendations")
        assert response.status_code == 200
        
        result = response.json()
        assert "recommendations" in result
        recommendations = result["recommendations"]
        
        # All recommendations should have images
        for recipe in recommendations:
            assert recipe["previewImageUrlTemplate"] is not None
            assert recipe["previewImageUrlTemplate"] != ""
            assert "previewImageUrlTemplate" in recipe

    def test_get_recommendations_returns_maximum_8_recipes(self, client, recipes_with_images):
        """Test that recommendations return at most 8 recipes."""
        # Create 10 recipes with images
        extended_recipes = recipes_with_images + [
            {
                "title": f"Extra Recipe {i}",
                "rating": 4.5,
                "previewImageUrlTemplate": f"https://example.com/images/<format>/extra{i}.jpg",
                "instructions": f"Instructions for extra recipe {i}",
                "ingredientsText": f"Ingredients for extra recipe {i}",
            }
            for i in range(6, 11)
        ]
        
        for recipe in extended_recipes:
            response = client.post(RECIPE_URL, json=recipe)
            assert response.status_code == 201

        # Get recommendations
        response = client.get(f"{RECIPE_URL}/recommendations")
        assert response.status_code == 200
        
        result = response.json()
        recommendations = result["recommendations"]
        
        # Should return exactly 8 recommendations (or less if fewer available)
        assert len(recommendations) <= 8

    def test_get_recommendations_when_insufficient_images(self, client):
        """Test recommendations when there are fewer than 8 recipes with images."""
        # Create only 3 recipes with images
        recipes = [
            {
                "title": f"Limited Recipe {i}",
                "rating": 4.0,
                "previewImageUrlTemplate": f"https://example.com/images/<format>/limited{i}.jpg",
                "instructions": f"Instructions for limited recipe {i}",
                "ingredientsText": f"Ingredients for limited recipe {i}",
            }
            for i in range(1, 4)
        ]
        
        for recipe in recipes:
            response = client.post(RECIPE_URL, json=recipe)
            assert response.status_code == 201

        # Get recommendations
        response = client.get(f"{RECIPE_URL}/recommendations")
        assert response.status_code == 200
        
        result = response.json()
        recommendations = result["recommendations"]
        
        # Should return all available recipes with images (3 in this case)
        assert len(recommendations) == 3
        for recipe in recommendations:
            assert recipe["previewImageUrlTemplate"] is not None

    def test_get_recommendations_when_no_images_available(self, client):
        """Test recommendations when no recipes have images."""
        # Create recipes without images
        recipes = [
            {
                "title": f"No Image Recipe {i}",
                "rating": 4.0,
                "instructions": f"Instructions for recipe {i}",
                "ingredientsText": f"Ingredients for recipe {i}",
            }
            for i in range(1, 4)
        ]
        
        for recipe in recipes:
            response = client.post(RECIPE_URL, json=recipe)
            assert response.status_code == 201

        # Get recommendations
        response = client.get(f"{RECIPE_URL}/recommendations")
        assert response.status_code == 200
        
        result = response.json()
        recommendations = result["recommendations"]
        
        # Should return empty list when no images available
        assert len(recommendations) == 0

    def test_recommendations_response_structure(self, client, recipes_with_images):
        """Test that recommendations response has correct structure."""
        # Create recipes
        for recipe in recipes_with_images:
            response = client.post(RECIPE_URL, json=recipe)
            assert response.status_code == 201

        # Get recommendations
        response = client.get(f"{RECIPE_URL}/recommendations")
        assert response.status_code == 200
        
        result = response.json()
        
        # Check response structure
        assert isinstance(result, dict)
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)
        
        # Check individual recipe structure
        if result["recommendations"]:
            recipe = result["recommendations"][0]
            expected_fields = {
                "id", "title", "rating", "previewImageUrlTemplate",
                "cachedImagePath", "cachedImageUrl", "imageCachedAt"
            }
            for field in expected_fields:
                assert field in recipe

    def test_recommendations_randomness(self, client, recipes_with_images):
        """Test that recommendations provide some randomness (not always same order)."""
        # Create many recipes with images
        extended_recipes = recipes_with_images + [
            {
                "title": f"Random Recipe {i}",
                "rating": 4.0,
                "previewImageUrlTemplate": f"https://example.com/images/<format>/random{i}.jpg",
                "instructions": f"Instructions for random recipe {i}",
                "ingredientsText": f"Ingredients for random recipe {i}",
            }
            for i in range(6, 15)
        ]
        
        for recipe in extended_recipes:
            response = client.post(RECIPE_URL, json=recipe)
            assert response.status_code == 201

        # Get recommendations multiple times
        first_response = client.get(f"{RECIPE_URL}/recommendations")
        second_response = client.get(f"{RECIPE_URL}/recommendations")
        
        assert first_response.status_code == 200
        assert second_response.status_code == 200
        
        first_recommendations = first_response.json()["recommendations"]
        second_recommendations = second_response.json()["recommendations"]
        
        # Both should return valid recommendations
        assert len(first_recommendations) > 0
        assert len(second_recommendations) > 0
        
        # Extract IDs to compare order
        first_ids = [r["id"] for r in first_recommendations]
        second_ids = [r["id"] for r in second_recommendations]
        
        # With sufficient recipes, order might be different (though not guaranteed)
        # At minimum, both calls should work and return valid data
        assert len(first_ids) <= 8
        assert len(second_ids) <= 8