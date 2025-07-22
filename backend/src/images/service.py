"""
Image storage service for downloading and storing recipe images permanently.

:module: images.service
"""
import hashlib
import os
from datetime import datetime, UTC
from pathlib import Path
from typing import Optional
import aiohttp
import aiofiles
from fastapi import HTTPException

from ..config import settings


class ImageStorageService:
    """Service for permanently storing external recipe images locally."""
    
    def __init__(self):
        self.storage_dir = Path(settings.IMAGE_STORAGE_DIR)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_image_path_and_filename(self, url: str, format_type: str = "crop-360x240") -> tuple[Path, str]:
        """
        Generate hierarchical directory structure and filename for an image.
        
        Uses the first 2 characters of the hash as subdirectories for better performance.
        Example: hash 'a1b2c3...' -> static/images/recipes/a1/b2/a1b2c3...jpg
        
        :param url: Original image URL template
        :param format_type: Image format type (e.g., 'crop-360x240')
        :returns: Tuple of (full_path, filename)
        """
        processed_url = url.replace('<format>', format_type)
        url_hash = hashlib.md5(processed_url.encode()).hexdigest()
        
        # Extract file extension from URL, default to .jpg
        extension = '.jpg'
        if '.' in processed_url:
            potential_ext = processed_url.split('.')[-1].split('?')[0].split('#')[0].lower()
            if potential_ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                extension = f'.{potential_ext}'
        
        filename = f"{url_hash}_{format_type}{extension}"
        
        # Create hierarchical directory structure using first 4 characters of hash
        # This creates up to 16^4 = 65,536 directories, each containing fewer images
        level1 = url_hash[:2]  # First 2 characters
        level2 = url_hash[2:4]  # Next 2 characters
        
        subdir_path = self.storage_dir / level1 / level2
        full_path = subdir_path / filename
        
        return full_path, filename
    
    async def store_image(self, recipe_id: str, image_url_template: str, 
                         format_type: str = "crop-360x240") -> dict[str, str]:
        """
        Download and permanently store an image from external URL.
        
        :param recipe_id: Recipe ID for logging purposes
        :param image_url_template: URL template with <format> placeholder
        :param format_type: Image format to download
        :returns: Dictionary with stored image info
        :raises HTTPException: If download fails
        """
        processed_url = image_url_template.replace('<format>', format_type)
        file_path, filename = self._get_image_path_and_filename(image_url_template, format_type)
        
        # Return existing stored image if it exists
        if file_path.exists():
            return {
                "stored_image_path": str(file_path),
                "stored_image_url": f"/api/v1/images/{filename}",
                "image_stored_at": datetime.now(UTC).isoformat()
            }
        
        # Create directory structure if it doesn't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Download the image
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(processed_url, timeout=30) as response:
                    if response.status != 200:
                        raise HTTPException(
                            status_code=400, 
                            detail=f"Failed to download image from {processed_url}: {response.status}"
                        )
                    
                    # Save image to hierarchical storage directory
                    async with aiofiles.open(file_path, 'wb') as file:
                        async for chunk in response.content.iter_chunked(8192):
                            await file.write(chunk)
                            
        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to download image from {processed_url}: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error storing image for recipe {recipe_id}: {str(e)}"
            )
        
        return {
            "stored_image_path": str(file_path),
            "stored_image_url": f"/api/v1/images/{filename}",
            "image_stored_at": datetime.now(UTC).isoformat()
        }
    
    def get_stored_image_path(self, filename: str) -> Optional[Path]:
        """
        Get path to stored image file using hierarchical directory structure.
        
        :param filename: Stored image filename (should start with hash)
        :returns: Path to image file if exists, None otherwise
        """
        # Extract hash from filename (format: hash_format.ext)
        if '_' not in filename:
            return None
            
        hash_part = filename.split('_')[0]
        if len(hash_part) < 4:
            return None
            
        # Reconstruct hierarchical path
        level1 = hash_part[:2]
        level2 = hash_part[2:4]
        file_path = self.storage_dir / level1 / level2 / filename
        
        return file_path if file_path.exists() else None
    
# Global service instance
image_storage_service = ImageStorageService()