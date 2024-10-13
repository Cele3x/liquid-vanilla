import pytest
from bson import ObjectId
import random
from backend.src.config import settings

RECIPE_URL = f"{settings.BASE_URL}/recipes"


@pytest.fixture
def valid_recipe():
    return {
        "title": "Test Recipe",
        "rating": 4.5,
        "sourceUrl": "https://example.com/recipes/12345",
        "previewImageUrlTemplate": "https://example.com/images/12345/<format>/image_description.jpg",
        "additionalDescription": "A delicious test recipe",
        "preparationTime": 15,
        "restingTime": 5,
        "source": "Test Source",
        "sourceId": "TS12345",
        "status": "active",
        "cookingTime": 30,
        "servings": 4,
        "sourceRating": 4.7,
        "subtitle": "Quick and easy",
        "createdAt": "2023-06-01T12:00:00",
        "sourceRatingVotes": 100,
        "tags": ["Vegetarisch", "Hauptspeise"],  # 6628c6289b0fefc37a4de8b8, 6628c62d9b0fefc37a4de8d9
        "ingredientGroups": [
            {
                "header": "Für das Gemüse:",
                "ingredients": [
                    {"ingredientId": "6628c6429b0fefc37a4de945", "unitId": "6628c6289b0fefc37a4de8a6", "amount": 500},
                    {"ingredientId": "6628c6289b0fefc37a4de8b1", "unitId": "6628c6289b0fefc37a4de8ab", "amount": 0}
                ]
            }
        ],
        "difficulty": 2,
        "sourceViewCount": 1000,
        "totalTime": 50,
        "userId": "6624e2a193986e2790e3c69f",
        "ingredientsText": "Ingredient 1, Ingredient 2, Ingredient 3",
        "instructions": "Step 1\nStep 2\nStep 3",
        "miscellaneousText": "Additional notes about the recipe"
    }


class TestRecipe:
    """Test suite for Recipe API endpoints."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, client):
        self.created_recipe_ids = []
        yield
        for recipe_id in self.created_recipe_ids:
            client.delete(f"{RECIPE_URL}/{recipe_id}")

    def create_recipe(self, client, recipe):
        response = client.post(RECIPE_URL, json=recipe)
        if response.status_code == 201:
            self.created_recipe_ids.append(response.json())
        return response

    class TestCreateRecipe:
        """Tests for creating recipes."""

        @pytest.mark.parametrize("invalid_recipe, expected_detail", [
            ({}, "title"),  # Empty recipe
            ({"title": ""}, "title"),  # Missing title
            ({"title": "X"}, "title"),  # Title too short
            ({"title": "X" * 101}, "title"),  # Title too long
        ])
        def test_create_invalid_recipe(self, client, invalid_recipe, expected_detail):
            """Test creating invalid recipes."""
            response = client.post(RECIPE_URL, json=invalid_recipe)
            assert response.status_code == 422
            assert expected_detail in response.json()["detail"][0]["loc"]

        def test_create_valid_recipe(self, client, valid_recipe):
            """Test creating a valid recipe."""
            response = client.post(RECIPE_URL, json=valid_recipe)
            assert response.status_code == 201
            assert ObjectId.is_valid(response.json())

        def test_create_minimal_valid_recipe(self, client, valid_recipe):
            """Test creating a recipe with minimal valid data."""
            minimal_recipe = {
                "title": valid_recipe["title"],
                "ingredientGroups": valid_recipe["ingredientGroups"],
                "instructions": valid_recipe["instructions"]
            }
            response = client.post(RECIPE_URL, json=minimal_recipe)
            assert response.status_code == 201
            assert ObjectId.is_valid(response.json())

    class TestGetRecipes:
        """Tests for retrieving recipes."""

        def test_get_multiple_recipes(self, client, valid_recipe):
            """Test retrieving multiple recipes."""
            for i in range(3):
                recipe = valid_recipe.copy()
                recipe["title"] = f"Test Recipe {i + 1}"
                client.post(RECIPE_URL, json=recipe)

            response = client.get(RECIPE_URL)
            assert response.status_code == 200
            result = response.json()
            assert isinstance(result, dict)
            assert len(result["recipes"]) >= 3
            assert all(isinstance(recipe, dict) for recipe in result['recipes'])
            expected_keys = {
                "id", "title", "rating", "sourceUrl", "previewImageUrlTemplate",
                "additionalDescription", "preparationTime", "restingTime", "source",
                "sourceId", "status", "cookingTime", "servings", "sourceRating",
                "subtitle", "createdAt", "sourceRatingVotes", "tags", "difficulty",
                "sourceViewCount", "totalTime", "userId", "ingredientsText",
                "instructions", "miscellaneousText", "ingredientGroups"
            }
            # Optionally, print the actual keys to help debug
            if not all(set(recipe.keys()) == expected_keys for recipe in result['recipes']):
                print("Actual keys in first recipe:", set(result['recipes'][0].keys()))
            assert all(set(recipe.keys()) == expected_keys for recipe in result['recipes'])

        def test_get_single_recipe(self, client, valid_recipe):
            """Test retrieving a single recipe."""
            create_response = client.post(RECIPE_URL, json=valid_recipe)
            recipe_id = create_response.json()

            response = client.get(f"{RECIPE_URL}/{recipe_id}")
            assert response.status_code == 200
            assert response.json() == {**valid_recipe, "id": recipe_id}

        def test_get_sorted_recipes_by_rating(self, client, valid_recipe):
            """Test retrieving recipes sorted by its rating as default (highest to lowest)."""
            created_recipes = []
            for i in range(5):
                recipe = valid_recipe.copy()
                recipe["title"] = f"Test Recipe {i + 1}"
                recipe["rating"] = random.uniform(0.0, 5.0)  # Get a random rating for each recipe
                response = client.post(RECIPE_URL, json=recipe)
                created_recipes.append(response.json())

            response = client.get(f"{RECIPE_URL}")
            assert response.status_code == 200

            result = response.json()
            retrieved_recipes = result["recipes"]
            assert len(retrieved_recipes) == 5

            # Check if the recipes are sorted by rating in descending order
            for i in range(len(retrieved_recipes) - 1):
                assert retrieved_recipes[i]['rating'] >= retrieved_recipes[i + 1]['rating']

            # Verify that all created recipes are in the response
            created_ids = set(recipe_id for recipe_id in created_recipes)
            retrieved_ids = set(recipe['id'] for recipe in retrieved_recipes)
            assert created_ids == retrieved_ids

            # Optional: Print the ratings to visualize the sorting
            print("Ratings in order:", [recipe['rating'] for recipe in retrieved_recipes])

        def test_get_recipes_with_pagination(self, client, valid_recipe):
            """Test retrieving recipes with pagination."""
            # Create 25 recipes
            for i in range(25):
                recipe = valid_recipe.copy()
                recipe["title"] = f"Test Recipe {i + 1}"
                recipe["rating"] = random.uniform(0.0, 5.0)
                client.post(RECIPE_URL, json=recipe)

            # Test first page
            response = client.get(f"{RECIPE_URL}?page=1&page_size=10")
            assert response.status_code == 200
            data = response.json()
            assert len(data["recipes"]) == 10
            assert data["page"] == 1
            assert data["page_size"] == 10
            assert data["total"] >= 25
            assert data["has_next"] is True
            assert data["has_previous"] is False

            # Test second page
            response = client.get(f"{RECIPE_URL}?page=2&page_size=10")
            assert response.status_code == 200
            data = response.json()
            assert len(data["recipes"]) == 10
            assert data["page"] == 2
            assert data["has_next"] is True
            assert data["has_previous"] is True

            # Test last page
            response = client.get(f"{RECIPE_URL}?page=3&page_size=10")
            assert response.status_code == 200
            data = response.json()
            assert len(data["recipes"]) == 5
            assert data["page"] == 3
            assert data["has_next"] is False
            assert data["has_previous"] is True

            # Test page size limit
            response = client.get(f"{RECIPE_URL}?page=1&page_size=101")
            assert response.status_code == 422

            # Verify sorting
            response = client.get(f"{RECIPE_URL}?page=1&page_size=25")
            data = response.json()
            recipes = data["recipes"]
            for i in range(len(recipes) - 1):
                assert recipes[i]['rating'] >= recipes[i + 1]['rating']

            # Test with default values
            response = client.get(f"{RECIPE_URL}")
            assert response.status_code == 200
            data = response.json()
            assert len(data["recipes"]) == 20  # Default page size
            assert data["page"] == 1
            assert data["page_size"] == 20

    class TestUpdateRecipe:
        """Tests for updating recipes."""

        def test_update_existing_recipe(self, client, valid_recipe):
            """Test updating an existing recipe."""
            create_response = client.post(RECIPE_URL, json=valid_recipe)
            recipe_id = create_response.json()

            updated_recipe = valid_recipe.copy()
            updated_recipe["title"] = "Updated Test Recipe"
            update_response = client.put(f"{RECIPE_URL}/{recipe_id}", json=updated_recipe)
            assert update_response.status_code == 204

            get_response = client.get(f"{RECIPE_URL}/{recipe_id}")
            assert get_response.status_code == 200
            assert get_response.json() == {**updated_recipe, "id": recipe_id}

        def test_update_nonexistent_recipe(self, client, valid_recipe):
            """Test updating a nonexistent recipe."""
            nonexistent_id = str(ObjectId())
            response = client.put(f"{RECIPE_URL}/{nonexistent_id}", json=valid_recipe)
            assert response.status_code == 404

        def test_update_with_invalid_data(self, client, valid_recipe):
            """Test updating a recipe with invalid data."""
            create_response = client.post(RECIPE_URL, json=valid_recipe)
            recipe_id = create_response.json()

            invalid_update = {"title": ""}  # Empty title is invalid
            update_response = client.put(f"{RECIPE_URL}/{recipe_id}", json=invalid_update)
            assert update_response.status_code == 422

    class TestDeleteRecipe:
        """Tests for deleting recipes."""

        def test_delete_existing_recipe(self, client, valid_recipe):
            """Test deleting an existing recipe."""
            create_response = client.post(RECIPE_URL, json=valid_recipe)
            recipe_id = create_response.json()

            delete_response = client.delete(f"{RECIPE_URL}/{recipe_id}")
            assert delete_response.status_code == 204

            get_response = client.get(f"{RECIPE_URL}/{recipe_id}")
            assert get_response.status_code == 404

        def test_delete_nonexistent_recipe(self, client):
            """Test deleting a nonexistent recipe."""
            nonexistent_id = str(ObjectId())
            response = client.delete(f"{RECIPE_URL}/{nonexistent_id}")
            assert response.status_code == 404
