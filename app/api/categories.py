"""
Category routes.
"""

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.middleware.auth import get_current_admin
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.response import success_response
from app.services.category_service import CategoryService
from app.core.cloudinary import upload_image
from app.models.admin import Admin

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("")
def list_categories(
    active_only: bool = False,
    db: Session = Depends(get_db),
):
    service = CategoryService(db)
    categories, total = service.get_all(active_only=active_only)
    return success_response(
        "Categories fetched",
        {"categories": [c.model_dump() for c in categories], "total": total},
    )


@router.get("/{slug}")
def get_category(slug: str, db: Session = Depends(get_db)):
    service = CategoryService(db)
    category = service.get_by_slug(slug)
    return success_response("Category fetched", category.model_dump())


@router.post("")
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    service = CategoryService(db)
    category = service.create(data)
    return success_response("Category created", category.model_dump())


@router.put("/{category_id}")
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    service = CategoryService(db)
    category = service.update(category_id, data)
    return success_response("Category updated", category.model_dump())


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    service = CategoryService(db)
    service.delete(category_id)
    return success_response("Category deleted")
