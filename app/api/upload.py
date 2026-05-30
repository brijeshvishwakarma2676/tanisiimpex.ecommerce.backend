"""
Upload routes - Cloudinary image management.
"""

from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.middleware.auth import get_current_admin
from app.core.cloudinary import upload_image, delete_image
from app.schemas.response import success_response, error_response
from app.models.admin import Admin

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/image")
async def upload(
    file: UploadFile = File(...),
    folder: str = Form("tanisiimpex"),
    admin: Admin = Depends(get_current_admin),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        return error_response("File must be an image")

    # 5MB limit
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        return error_response("File size must be less than 5MB")

    await file.seek(0)
    result = await upload_image(file, folder=folder)
    return success_response("Image uploaded", result)


@router.delete("/image")
def delete(
    public_id: str,
    admin: Admin = Depends(get_current_admin),
):
    success = delete_image(public_id)
    if success:
        return success_response("Image deleted")
    return error_response("Failed to delete image")
