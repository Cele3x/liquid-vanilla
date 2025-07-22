import pytest
from bson import ObjectId
from src.config import settings

TAG_URL = f"{settings.BASE_URL}/tags"

@pytest.fixture
def valid_tag():
    return {
        "name": "Test Tag"
    }

class TestTag:
    """Test suite for Tag API endpoints."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, client):
        self.created_tag_ids = []
        yield
        for tag_id in self.created_tag_ids:
            client.delete(f"{TAG_URL}/{tag_id}")

    def create_tag(self, client, tag):
        response = client.post(TAG_URL, json=tag)
        if response.status_code == 201:
            self.created_tag_ids.append(response.json())
        return response

    def test_get_all_tags(self, client, valid_tag):
        """Test retrieving all tags."""
        # Create tags
        tags = [
            {**valid_tag, "name": "Tag1"},
            {**valid_tag, "name": "Tag2"},
            {**valid_tag, "name": "Tag3"}
        ]

        for tag in tags:
            response = self.create_tag(client, tag)
            assert response.status_code == 201

        # Get all tags
        response = client.get(TAG_URL)
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(tag, dict) for tag in result)
        assert all("name" in tag for tag in result)

    def test_create_tag(self, client, valid_tag):
        """Test creating a new tag."""
        response = self.create_tag(client, valid_tag)
        assert response.status_code == 201
        assert ObjectId.is_valid(response.json())
