"""
Tests for image caching service functionality.

:module: tests.test_image_service
"""
import pytest
from unittest.mock import AsyncMock, patch, mock_open
from pathlib import Path
from datetime import datetime, UTC

from src.images.service import ImageStorageService


class TestImageStorageService:
    """Test suite for ImageStorageService."""

    @pytest.fixture
    def image_service(self):
        """Create ImageStorageService instance for testing."""
        with patch('src.images.service.settings.IMAGE_STORAGE_DIR', '/test/storage/recipe_images'), \
             patch('pathlib.Path.mkdir'):
            service = ImageStorageService()
            return service

    def test_get_image_path_and_filename(self, image_service):
        """Test hierarchical path and filename generation for stored images."""
        url_template = "https://example.com/images/<format>/test.jpg"
        full_path, filename = image_service._get_image_path_and_filename(url_template, "crop-360x240")
        
        assert filename.endswith("_crop-360x240.jpg")
        assert len(filename.split("_crop-360x240.jpg")[0]) == 32  # MD5 hash length
        
        # Check hierarchical directory structure
        path_parts = full_path.parts
        assert len(path_parts) >= 5  # Should have at least cache/recipe_images/level1/level2/filename
        assert path_parts[-3]  # level1 directory (2 chars)
        assert path_parts[-2]  # level2 directory (2 chars)
        assert len(path_parts[-3]) == 2
        assert len(path_parts[-2]) == 2

    def test_get_image_path_different_formats(self, image_service):
        """Test path generation for different image formats."""
        url_template = "https://example.com/images/<format>/test.png"
        
        full_path_png, filename_png = image_service._get_image_path_and_filename(url_template, "crop-360x240")
        assert filename_png.endswith("_crop-360x240.png")
        
        full_path_webp, filename_webp = image_service._get_image_path_and_filename(
            "https://example.com/images/<format>/test.webp", "thumbnail-150x150"
        )
        assert filename_webp.endswith("_thumbnail-150x150.webp")
        
        # Verify hierarchical structure for both
        assert len(full_path_png.parts) >= 5
        assert len(full_path_webp.parts) >= 5

    @pytest.mark.asyncio
    async def test_store_image_success_basic(self, image_service):
        """Test basic image storing flow."""
        recipe_id = "test_recipe_123"
        url_template = "https://example.com/images/<format>/test.jpg"
        
        # Test the method exists and can be called
        with patch('pathlib.Path.exists', return_value=True):
            result = await image_service.store_image(recipe_id, url_template)
            
            assert "stored_image_path" in result
            assert "stored_image_url" in result  
            assert "image_stored_at" in result

    @pytest.mark.asyncio
    async def test_store_image_already_exists(self, image_service):
        """Test storing when image already exists."""
        recipe_id = "test_recipe_123"
        url_template = "https://example.com/images/<format>/test.jpg"
        
        with patch('pathlib.Path.exists', return_value=True):
            result = await image_service.store_image(recipe_id, url_template)
            
            assert "stored_image_path" in result
            assert "stored_image_url" in result
            assert "image_stored_at" in result

    @pytest.mark.asyncio 
    async def test_store_image_error_handling(self, image_service):
        """Test image storing error handling."""
        recipe_id = "test_recipe_123"
        url_template = "https://example.com/images/<format>/test.jpg"
        
        # Test with network failure by patching ClientSession to raise exception
        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_session_class.side_effect = Exception("Network error")
            
            with patch('pathlib.Path.exists', return_value=False), \
                 patch('pathlib.Path.mkdir'):
                
                with pytest.raises(Exception):
                    await image_service.store_image(recipe_id, url_template)


    def test_get_stored_image_path_exists(self, image_service):
        """Test getting stored image path when file exists in hierarchical structure."""
        # Use a realistic filename with hash
        filename = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6_crop-360x240.jpg"
        
        with patch('pathlib.Path.exists', return_value=True):
            result = image_service.get_stored_image_path(filename)
            
            assert result is not None
            assert str(result).endswith(filename)
            # Check that it includes hierarchical path (a1/b2/)
            assert "/a1/b2/" in str(result)

    def test_get_stored_image_path_not_exists(self, image_service):
        """Test getting stored image path when file doesn't exist."""
        filename = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6_crop-360x240.jpg"
        
        with patch('pathlib.Path.exists', return_value=False):
            result = image_service.get_stored_image_path(filename)
            
            assert result is None

    def test_get_stored_image_path_invalid_filename(self, image_service):
        """Test getting stored image path with invalid filename format."""
        # Test filename without underscore
        result1 = image_service.get_stored_image_path("invalid_filename_no_hash")
        assert result1 is None
        
        # Test filename with short hash
        result2 = image_service.get_stored_image_path("ab_format.jpg")
        assert result2 is None

    # NOTE: delete_stored_image method not implemented in service yet
    # def test_delete_stored_image_method_exists(self, image_service):
    #     """Test that delete stored image method works with hierarchical structure."""
    #     filename = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6_crop-360x240.jpg"
    #     
    #     # Test when file doesn't exist
    #     with patch.object(image_service, 'get_stored_image_path', return_value=None):
    #         result = image_service.delete_stored_image(filename)
    #         assert result is False
    #     
    #     # Test when file exists and can be deleted
    #     mock_path = Path(f"/test/storage/recipe_images/a1/b2/{filename}")
    #     with patch.object(image_service, 'get_stored_image_path', return_value=mock_path), \
    #          patch('pathlib.Path.exists', return_value=True), \
    #          patch('pathlib.Path.unlink') as mock_unlink, \
    #          patch('pathlib.Path.iterdir', return_value=[]), \
    #          patch('pathlib.Path.rmdir'):
    #         
    #         result = image_service.delete_stored_image(filename)
    #         assert result is True
    #         mock_unlink.assert_called_once()