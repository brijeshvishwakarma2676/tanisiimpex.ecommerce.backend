"""
Product routes.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.middleware.auth import get_current_admin
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.response import success_response
from app.services.product_service import ProductService
from app.models.admin import Admin

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("")
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    result = service.get_all(
        page=page,
        page_size=page_size,
        search=search,
        category_id=category_id,
        featured=featured,
        active_only=True,
    )
    return success_response("Products fetched", result.model_dump())


@router.get("/admin")
def list_products_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    service = ProductService(db)
    result = service.get_all(
        page=page,
        page_size=page_size,
        search=search,
        category_id=category_id,
        featured=featured,
        admin=True,
    )
    return success_response("Products fetched", result.model_dump())


@router.get("/featured")
def get_featured(
    limit: int = Query(8, ge=1, le=20),
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    products = service.get_featured(limit)
    return success_response(
        "Featured products fetched",
        [p.model_dump() for p in products],
    )


@router.get("/{slug}")
def get_product(slug: str, db: Session = Depends(get_db)):
    service = ProductService(db)
    product = service.get_by_slug(slug)
    return success_response("Product fetched", product.model_dump())


@router.get("/{slug}/related")
def get_related(
    slug: str,
    limit: int = Query(4, ge=1, le=10),
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    product = service.get_by_slug(slug)
    related = service.get_related(product.id, product.category_id, limit)
    return success_response(
        "Related products fetched",
        [p.model_dump() for p in related],
    )


@router.post("")
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    service = ProductService(db)
    product = service.create(data)
    return success_response("Product created", product.model_dump())


@router.put("/{product_id}")
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    service = ProductService(db)
    product = service.update(product_id, data)
    return success_response("Product updated", product.model_dump())


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    service = ProductService(db)
    service.delete(product_id)
    return success_response("Product deleted")
