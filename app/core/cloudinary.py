"""
Cloudinary integration for image upload and management.
"""

import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

from app.core.config import settings


def configure_cloudinary():
    """Initialize Cloudinary with credentials."""
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )


async def upload_image(file: UploadFile, folder: str = "tanisiimpex") -> dict:
    """
    Upload an image to Cloudinary.
    Returns dict with 'url' and 'public_id'.
    """
    configure_cloudinary()
    contents = await file.read()
    result = cloudinary.uploader.upload(
        contents,
        folder=folder,
        resource_type="image",
        transformation=[
            {"quality": "auto:good", "fetch_format": "auto"},
        ],
    )
    return {
        "url": result["secure_url"],
        "public_id": result["public_id"],
    }


def delete_image(public_id: str) -> bool:
    """Delete an image from Cloudinary by its public_id."""
    configure_cloudinary()
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result.get("result") == "ok"
    except Exception:
        return False
