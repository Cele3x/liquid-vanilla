"""
Test utilities for shared functionality across test files.

:module: tests.test_utils
"""
import pytest
from typing import List
from src.config import settings


class TestResourceManager:
    """Manager for test resources that need cleanup after tests."""
    
    def __init__(self, client, resource_type: str):
        """
        Initialize the resource manager.
        
        :param client: FastAPI test client
        :param resource_type: Type of resource ('recipes', 'tags', etc.)
        """
        self.client = client
        self.resource_type = resource_type
        self.base_url = f"{settings.BASE_URL}/{resource_type}"
        self.created_resource_ids: List[str] = []
    
    def create_resource(self, resource_data: dict):
        """
        Create a resource and track it for cleanup.
        
        :param resource_data: Data for the resource to create
        :returns: Response from the creation request
        """
        response = self.client.post(self.base_url, json=resource_data)
        if response.status_code == 201:
            self.created_resource_ids.append(response.json())
        return response
    
    def cleanup(self):
        """Clean up all created resources."""
        for resource_id in self.created_resource_ids:
            self.client.delete(f"{self.base_url}/{resource_id}")
        self.created_resource_ids.clear()


class RecipeTestMixin:
    """Mixin class for recipe-related tests with automatic cleanup."""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, client):
        """Set up test environment and clean up after tests."""
        self.created_recipe_ids = []
        yield
        for recipe_id in self.created_recipe_ids:
            client.delete(f"{settings.BASE_URL}/recipes/{recipe_id}")

    def create_recipe(self, client, recipe):
        """
        Create a recipe and track it for cleanup.
        
        :param client: FastAPI test client
        :param recipe: Recipe data to create
        :returns: Response from the creation request
        """
        response = client.post(f"{settings.BASE_URL}/recipes", json=recipe)
        if response.status_code == 201:
            self.created_recipe_ids.append(response.json())
        return response


class TagTestMixin:
    """Mixin class for tag-related tests with automatic cleanup."""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, client):
        """Set up test environment and clean up after tests."""
        self.created_tag_ids = []
        yield
        for tag_id in self.created_tag_ids:
            client.delete(f"{settings.BASE_URL}/tags/{tag_id}")

    def create_tag(self, client, tag):
        """
        Create a tag and track it for cleanup.
        
        :param client: FastAPI test client
        :param tag: Tag data to create
        :returns: Response from the creation request
        """
        response = client.post(f"{settings.BASE_URL}/tags", json=tag)
        if response.status_code == 201:
            self.created_tag_ids.append(response.json())
        return response


def resource_cleanup_fixture(resource_type: str):
    """
    Create a pytest fixture for resource cleanup.
    
    :param resource_type: Type of resource ('recipes', 'tags', etc.)
    :returns: Pytest fixture function
    """
    @pytest.fixture(autouse=True)
    def cleanup_fixture(client):
        """Fixture for cleaning up created resources."""
        created_ids = []
        
        def create_and_track(resource_data):
            response = client.post(f"{settings.BASE_URL}/{resource_type}", json=resource_data)
            if response.status_code == 201:
                created_ids.append(response.json())
            return response
        
        # Provide the create function to the test
        yield create_and_track
        
        # Cleanup after the test
        for resource_id in created_ids:
            client.delete(f"{settings.BASE_URL}/{resource_type}/{resource_id}")
    
    return cleanup_fixture