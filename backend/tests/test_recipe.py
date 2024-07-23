import pytest
from bson import ObjectId
from fastapi.testclient import TestClient
from backend.src.config import settings

RECIPE_URL = f"{settings.BASE_URL}/recipes"


@pytest.fixture
def valid_recipe():
    return {"name": "Test Recipe", "description": "This is a test recipe"}


@pytest.fixture
def client(client: TestClient):
    return client


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
            ({}, "name"),  # Empty recipe
            ({"name": ""}, "name"),  # Missing name
            ({"name": "X"}, "name"),  # Name too short
            ({"name": "X" * 101}, "name"),  # Name too long
            ({"name": "Test Recipe", "description": "X" * 257}, "description"),  # Description too long
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

    class TestGetRecipes:
        """Tests for retrieving recipes."""

        def test_get_multiple_recipes(self, client, valid_recipe):
            """Test retrieving multiple recipes."""
            for i in range(3):
                recipe = valid_recipe.copy()
                recipe["name"] = f"Test Recipe {i + 1}"
                client.post(RECIPE_URL, json=recipe)

            response = client.get(RECIPE_URL)
            assert response.status_code == 200
            recipes = response.json()
            assert len(recipes) >= 3
            assert all(isinstance(recipe, dict) for recipe in recipes)
            assert all(set(recipe.keys()) == {"id", "name", "description"} for recipe in recipes)

        def test_get_single_recipe(self, client, valid_recipe):
            """Test retrieving a single recipe."""
            create_response = client.post(RECIPE_URL, json=valid_recipe)
            recipe_id = create_response.json()

            response = client.get(f"{RECIPE_URL}/{recipe_id}")
            assert response.status_code == 200
            assert response.json() == {**valid_recipe, "id": recipe_id}

    class TestUpdateRecipe:
        """Tests for updating recipes."""

        def test_update_existing_recipe(self, client, valid_recipe):
            """Test updating an existing recipe."""
            create_response = client.post(RECIPE_URL, json=valid_recipe)
            recipe_id = create_response.json()

            updated_recipe = {
                "name": "Updated Test Recipe",
                "description": "This is an updated test recipe",
            }
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

            invalid_update = {"name": ""}  # Empty name is invalid
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
