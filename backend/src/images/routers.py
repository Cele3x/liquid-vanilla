"""
Image routing endpoints for serving cached recipe images.

:module: images.routers
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from typing import Dict, Any
from .service import image_storage_service

router = APIRouter()


@router.get("/{filename}")
async def get_stored_image(filename: str):
    """
    Serve a stored image file.
    
    :param filename: Name of the stored image file
    :returns: FileResponse with the image
    :raises HTTPException: If image not found
    """
    file_path = image_storage_service.get_stored_image_path(filename)
    
    if not file_path:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Determine media type based on file extension
    extension = filename.split('.')[-1].lower()
    media_type_map = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg', 
        'png': 'image/png',
        'webp': 'image/webp',
        'gif': 'image/gif'
    }
    
    media_type = media_type_map.get(extension, 'image/jpeg')
    
    return FileResponse(
        path=file_path,
        media_type=media_type,
        headers={"Cache-Control": "public, max-age=86400"}  # Cache for 24 hours
    )


@router.get("/storage/stats")
async def get_storage_stats() -> Dict[str, Any]:
    """
    Get statistics about the image storage.
    
    :returns: Dictionary with storage statistics
    """
    storage_dir = Path(image_storage_service.storage_dir)
    
    if not storage_dir.exists():
        return {
            "total_images": 0,
            "total_size_bytes": 0,
            "total_size_mb": 0,
            "storage_directory": str(storage_dir),
            "storage_exists": False
        }
    
    total_images = 0
    total_size = 0
    
    # Count all image files recursively
    for file_path in storage_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            total_images += 1
            total_size += file_path.stat().st_size
    
    return {
        "total_images": total_images,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "storage_directory": str(storage_dir),
        "storage_exists": True
    }