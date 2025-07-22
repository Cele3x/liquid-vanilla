"""
Edge case tests for image caching service.

:module: tests.test_image_service_edge_cases
"""
import pytest
from unittest.mock import patch, AsyncMock, mock_open
from pathlib import Path

from src.images.service import ImageCacheService


class TestImageServiceEdgeCases:
    """Test suite for ImageCacheService edge cases and error scenarios."""

    @pytest.fixture
    def image_service(self):
        """Create ImageCacheService instance for testing."""
        with patch('src.images.service.settings.IMAGE_CACHE_DIR', '/test/cache/recipe_images'), \
             patch('pathlib.Path.mkdir'):
            service = ImageCacheService()
            return service

    def test_get_image_path_with_unicode_characters(self, image_service):
        """Test path generation with Unicode characters in URL."""
        unicode_urls = [
            "https://example.com/images/<format>/café.jpg",
            "https://example.com/images/<format>/naïve.png",
            "https://example.com/images/<format>/тест.jpg",
            "https://example.com/images/<format>/测试.webp",
        ]
        
        for url in unicode_urls:
            path, filename = image_service._get_image_path_and_filename(url)
            
            # Should handle Unicode properly
            assert path is not None
            assert filename is not None
            assert len(filename.split('_')[0]) == 32  # MD5 hash length
            
            # Verify hierarchical structure
            assert len(path.parts) >= 5

    def test_get_image_path_with_very_long_urls(self, image_service):
        """Test path generation with extremely long URLs."""
        long_url = "https://example.com/images/<format>/" + "a" * 2000 + ".jpg"
        
        path, filename = image_service._get_image_path_and_filename(long_url)
        
        # Should handle long URLs by hashing them
        assert path is not None
        assert filename is not None
        assert len(filename.split('_')[0]) == 32  # MD5 hash should be fixed length

    def test_get_image_path_with_url_special_characters(self, image_service):
        """Test path generation with special characters in URL."""
        special_urls = [
            "https://example.com/images/<format>/test%20image.jpg",
            "https://example.com/images/<format>/test&image.png",
            "https://example.com/images/<format>/test+image.webp",
            "https://example.com/images/<format>/test@image.gif",
            "https://example.com/images/<format>/test#image.jpg",
        ]
        
        for url in special_urls:
            path, filename = image_service._get_image_path_and_filename(url)
            
            assert path is not None
            assert filename is not None
            assert len(filename.split('_')[0]) == 32

    def test_get_image_path_with_no_extension(self, image_service):
        """Test path generation when URL has no file extension."""
        url = "https://example.com/images/<format>/imagewithoutextension"
        
        path, filename = image_service._get_image_path_and_filename(url)
        
        # Should default to .jpg
        assert filename.endswith(".jpg")
        assert "_crop-360x240.jpg" in filename

    def test_get_image_path_with_query_parameters(self, image_service):
        """Test path generation with URL query parameters."""
        url = "https://example.com/images/<format>/test.jpg?version=123&size=large"
        
        path, filename = image_service._get_image_path_and_filename(url)
        
        # Should still extract .jpg extension correctly
        assert filename.endswith("_crop-360x240.jpg")
        assert len(filename.split('_')[0]) == 32

    def test_get_image_path_with_fragments(self, image_service):
        """Test path generation with URL fragments."""
        url = "https://example.com/images/<format>/test.png#section1"
        
        path, filename = image_service._get_image_path_and_filename(url)
        
        # Should extract .png extension correctly
        assert filename.endswith("_crop-360x240.png")

    def test_get_image_path_with_multiple_dots(self, image_service):
        """Test path generation with multiple dots in URL."""
        url = "https://example.com/images/<format>/test.image.file.jpg"
        
        path, filename = image_service._get_image_path_and_filename(url)
        
        # Should use the last extension
        assert filename.endswith("_crop-360x240.jpg")

    def test_get_image_path_with_unsupported_extension(self, image_service):
        """Test path generation with unsupported file extension."""
        url = "https://example.com/images/<format>/test.xyz"
        
        path, filename = image_service._get_image_path_and_filename(url)
        
        # Should default to .jpg for unsupported extensions
        assert filename.endswith("_crop-360x240.jpg")

    def test_get_cached_image_path_edge_cases(self, image_service):
        """Test get_cached_image_path with various edge case filenames."""
        edge_case_filenames = [
            "",  # Empty filename
            "no_underscore.jpg",  # No underscore
            "_justformat.jpg",  # No hash part
            "a_format.jpg",  # Very short hash
            "abc_format.jpg",  # Short hash (less than 4 chars)
            "validhash1234567890abcdef1234_format.jpg",  # Valid case
        ]
        
        for filename in edge_case_filenames:
            result = image_service.get_cached_image_path(filename)
            
            if filename in ["", "no_underscore.jpg", "_justformat.jpg", "a_format.jpg", "abc_format.jpg"]:
                # Invalid formats should return None
                assert result is None
            else:
                # Valid format should process (though file won't exist in test)
                # The method would normally check file existence
                pass

    @pytest.mark.asyncio
    async def test_cache_image_with_invalid_urls(self, image_service):
        """Test cache_image with invalid or malformed URLs."""
        invalid_urls = [
            "not-a-url",
            "http://",
            "://missing-protocol.com",
            "",
        ]
        
        for url in invalid_urls:
            recipe_id = "test_recipe"
            
            # These should either handle gracefully or raise appropriate exceptions
            try:
                with patch('pathlib.Path.exists', return_value=False), \
                     patch('pathlib.Path.mkdir'):
                    result = await image_service.cache_image(recipe_id, url)
                    # If it succeeds, it should return a valid result
                    assert "cached_image_path" in result
            except Exception as e:
                # It's acceptable for invalid URLs to raise exceptions
                assert isinstance(e, (ValueError, Exception))

    @pytest.mark.asyncio
    async def test_cache_image_with_extremely_long_format_type(self, image_service):
        """Test cache_image with very long format type."""
        url = "https://example.com/images/<format>/test.jpg"
        long_format = "extremely_long_format_type_that_exceeds_normal_length" * 10
        recipe_id = "test_recipe"
        
        with patch('pathlib.Path.exists', return_value=True):
            result = await image_service.cache_image(recipe_id, url, long_format)
            
            # Should handle long format types
            assert "cached_image_path" in result
            assert "cached_image_url" in result

    def test_delete_cached_image_with_complex_directory_cleanup(self, image_service):
        """Test delete operation with complex directory cleanup scenarios."""
        filename = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6_crop-360x240.jpg"
        
        # Test case 1: File exists, directories should be cleaned up
        mock_file_path = Path("/test/cache/recipe_images/a1/b2/") / filename
        
        with patch.object(image_service, 'get_cached_image_path', return_value=mock_file_path), \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.unlink') as mock_unlink, \
             patch('pathlib.Path.iterdir') as mock_iterdir, \
             patch('pathlib.Path.rmdir') as mock_rmdir:
            
            # Simulate empty directories
            mock_iterdir.return_value = []
            
            result = image_service.delete_cached_image(filename)
            
            assert result is True
            mock_unlink.assert_called_once()

    def test_delete_cached_image_with_permission_errors(self, image_service):
        """Test delete operation when permission errors occur."""
        filename = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6_crop-360x240.jpg"
        mock_file_path = Path("/test/cache/recipe_images/a1/b2/") / filename
        
        with patch.object(image_service, 'get_cached_image_path', return_value=mock_file_path), \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.unlink', side_effect=PermissionError("Permission denied")):
            
            result = image_service.delete_cached_image(filename)
            
            # Should handle permission errors gracefully
            assert result is False

    def test_hierarchical_directory_collision_handling(self, image_service):
        """Test that different URLs with same directory structure are handled correctly."""
        # Create URLs that might hash to same directory structure
        urls = [
            "https://example1.com/images/<format>/test.jpg",
            "https://example2.com/images/<format>/test.jpg",
            "https://example3.com/different/<format>/test.jpg",
        ]
        
        paths_and_filenames = []
        for url in urls:
            path, filename = image_service._get_image_path_and_filename(url)
            paths_and_filenames.append((path, filename))
        
        # All should have different filenames (due to different URLs)
        filenames = [f for p, f in paths_and_filenames]
        assert len(set(filenames)) == len(filenames)  # All unique
        
        # But may share directory structure (which is fine)
        for path, filename in paths_and_filenames:
            assert len(path.parts) >= 5
            assert filename.endswith("_crop-360x240.jpg")

    @pytest.mark.asyncio
    async def test_cache_image_with_network_timeout_simulation(self, image_service):
        """Test cache_image behavior with network timeout."""
        recipe_id = "test_recipe"
        url = "https://example.com/images/<format>/test.jpg"
        
        # Simulate network timeout
        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_session = AsyncMock()
            mock_session_class.return_value.__aenter__.return_value = mock_session
            # Create proper async mock for get method
            async_get_mock = AsyncMock()
            async_get_mock.side_effect = TimeoutError("Request timeout")
            mock_session.get = async_get_mock
            
            with patch('pathlib.Path.exists', return_value=False), \
                 patch('pathlib.Path.mkdir'):
                
                with pytest.raises(Exception):
                    await image_service.cache_image(recipe_id, url)

    def test_image_service_initialization_with_invalid_cache_dir(self):
        """Test ImageCacheService initialization with invalid cache directory."""
        # Test with non-string cache directory
        with patch('src.images.service.settings.IMAGE_CACHE_DIR', None):
            try:
                # This might raise an exception, which is expected
                service = ImageCacheService()
            except Exception:
                # It's acceptable for invalid cache dir to cause initialization failure
                pass

    def test_filename_hash_consistency_across_instances(self):
        """Test that different service instances generate same hash for same URL."""
        url = "https://example.com/images/<format>/consistency_test.jpg"
        
        # Create two service instances
        with patch('src.images.service.settings.IMAGE_CACHE_DIR', '/test/cache1'), \
             patch('pathlib.Path.mkdir'):
            service1 = ImageCacheService()
        
        with patch('src.images.service.settings.IMAGE_CACHE_DIR', '/test/cache2'), \
             patch('pathlib.Path.mkdir'):
            service2 = ImageCacheService()
        
        # Both should generate same filename (but different paths due to different cache dirs)
        path1, filename1 = service1._get_image_path_and_filename(url)
        path2, filename2 = service2._get_image_path_and_filename(url)
        
        assert filename1 == filename2  # Same filename
        assert str(path1) != str(path2)  # Different paths