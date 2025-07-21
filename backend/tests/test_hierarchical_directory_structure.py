"""
Tests to demonstrate the hierarchical directory structure for image caching.

:module: tests.test_hierarchical_directory_structure
"""
import pytest
from unittest.mock import patch

from src.images.service import ImageCacheService


class TestHierarchicalDirectoryStructure:
    """Test suite to demonstrate hierarchical directory structure benefits."""

    @pytest.fixture
    def image_service(self):
        """Create ImageCacheService instance for testing."""
        with patch('src.images.service.settings.IMAGE_CACHE_DIR', '/cache/recipe_images'), \
             patch('pathlib.Path.mkdir'):
            service = ImageCacheService()
            return service

    def test_directory_structure_distribution(self, image_service):
        """Test that different URLs create well-distributed directory structure."""
        # Test URLs that would create different hash prefixes
        test_urls = [
            "https://example.com/images/<format>/recipe1.jpg",
            "https://example.com/images/<format>/recipe2.jpg", 
            "https://different.com/images/<format>/recipe3.jpg",
            "https://another.com/images/<format>/recipe4.jpg",
            "https://example.com/different/<format>/recipe5.jpg"
        ]
        
        paths_and_filenames = []
        for url in test_urls:
            path, filename = image_service._get_image_path_and_filename(url)
            paths_and_filenames.append((path, filename))
        
        # Verify each has proper hierarchical structure
        for path, filename in paths_and_filenames:
            path_parts = path.parts
            
            # Should have structure: /cache/recipe_images/XX/YY/filename
            assert len(path_parts) >= 5
            assert path_parts[-4] == "recipe_images"
            assert path_parts[-3]  # level1 (2 chars)
            assert path_parts[-2]  # level2 (2 chars) 
            assert path_parts[-1] == filename
            
            # Verify subdirectory naming
            level1 = path_parts[-3]
            level2 = path_parts[-2]
            assert len(level1) == 2
            assert len(level2) == 2
            assert all(c in '0123456789abcdef' for c in level1.lower())
            assert all(c in '0123456789abcdef' for c in level2.lower())

    def test_hash_based_distribution_consistency(self, image_service):
        """Test that same URL always maps to same directory structure."""
        url = "https://example.com/images/<format>/consistent.jpg"
        
        # Get path multiple times
        path1, filename1 = image_service._get_image_path_and_filename(url)
        path2, filename2 = image_service._get_image_path_and_filename(url)
        path3, filename3 = image_service._get_image_path_and_filename(url)
        
        # Should always be identical
        assert path1 == path2 == path3
        assert filename1 == filename2 == filename3

    def test_directory_structure_scalability_simulation(self, image_service):
        """Test directory structure can handle many files efficiently."""
        # Simulate many different image URLs
        simulated_urls = []
        for i in range(1000):
            simulated_urls.append(f"https://example.com/images/<format>/recipe_{i:04d}.jpg")
        
        directory_distribution = {}
        
        for url in simulated_urls:
            path, filename = image_service._get_image_path_and_filename(url)
            # Extract level1/level2 directory structure
            level1_level2 = f"{path.parts[-3]}/{path.parts[-2]}"
            
            if level1_level2 not in directory_distribution:
                directory_distribution[level1_level2] = 0
            directory_distribution[level1_level2] += 1
        
        # With 1000 files and good hash distribution, should have many directories
        # Each directory should contain relatively few files
        assert len(directory_distribution) > 50  # Should create many subdirectories
        
        # No single directory should contain too many files (good distribution)
        max_files_per_dir = max(directory_distribution.values())
        assert max_files_per_dir < 100  # Should be well distributed

    def test_directory_cleanup_functionality(self, image_service):
        """Test that directory cleanup works with hierarchical structure."""
        filename = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6_crop-360x240.jpg"
        
        # Mock the path structure
        from pathlib import Path
        mock_file_path = Path("/cache/recipe_images/a1/b2") / filename
        mock_level2_dir = mock_file_path.parent  # /cache/recipe_images/a1/b2
        mock_level1_dir = mock_level2_dir.parent  # /cache/recipe_images/a1
        
        with patch.object(image_service, 'get_cached_image_path', return_value=mock_file_path), \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.unlink') as mock_unlink, \
             patch('pathlib.Path.iterdir') as mock_iterdir, \
             patch('pathlib.Path.rmdir') as mock_rmdir:
            
            # Simulate empty directories after file deletion
            mock_iterdir.return_value = []
            
            result = image_service.delete_cached_image(filename)
            
            assert result is True
            mock_unlink.assert_called_once()
            # Should attempt to clean up empty directories
            assert mock_rmdir.call_count >= 1

    def test_directory_structure_documentation_example(self, image_service):
        """Test that provides a clear example of the directory structure."""
        # Example URL that would create a predictable hash
        url = "https://example.com/images/<format>/sample.jpg"
        path, filename = image_service._get_image_path_and_filename(url)
        
        # Extract the directory structure
        path_parts = path.parts
        level1 = path_parts[-3]
        level2 = path_parts[-2]
        
        print(f"\nDirectory structure example:")
        print(f"Original URL: {url}")
        print(f"Processed URL: {url.replace('<format>', 'crop-360x240')}")
        print(f"Generated filename: {filename}")
        print(f"Full path: {path}")
        print(f"Directory structure: cache/recipe_images/{level1}/{level2}/{filename}")
        print(f"This creates max 65,536 directories (16^4) instead of one flat directory")
        
        # Verify the structure
        assert len(level1) == 2
        assert len(level2) == 2
        assert filename.endswith("_crop-360x240.jpg")
        assert str(path).endswith(f"{level1}/{level2}/{filename}")