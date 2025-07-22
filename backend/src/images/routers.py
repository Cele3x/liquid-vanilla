"""
Image routing endpoints for serving cached recipe images.

:module: images.routers
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from .service import image_cache_service

router = APIRouter()


@router.get("/{filename}")
async def get_cached_image(filename: str):
    """
    Serve a cached image file.
    
    :param filename: Name of the cached image file
    :returns: FileResponse with the image
    :raises HTTPException: If image not found
    """
    file_path = image_cache_service.get_cached_image_path(filename)
    
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