"""
Product service - business logic.
"""

from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from slugify import slugify

from app.models.product import Product
from app.repositories.product_repo import ProductRepository
from app.repositories.category_repo import CategoryRepository
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductAdminResponse,
    ProductListResponse,
)


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)
        self.category_repo = CategoryRepository(db)

    def _to_response(self, product: Product, admin: bool = False) -> ProductResponse:
        """Convert product model to response schema."""
        cls = ProductAdminResponse if admin else ProductResponse
        return cls(
            id=product.id,
            category_id=product.category_id,
            name=product.name,
            slug=product.slug,
            sku=product.sku,
            short_description=product.short_description,
            description=product.description,
            moq=product.moq,
            stock_status=product.stock_status,
            featured=product.featured,
            image=product.image,
            gallery_images=product.gallery_images or [],
            status=product.status,
            created_at=product.created_at,
            updated_at=product.updated_at,
            category_name=product.category.name if product.category else None,
            **(
                {"price": float(product.price) if product.price else None,
                 "wholesale_price": float(product.wholesale_price) if product.wholesale_price else None}
                if admin else {}
            ),
        )

    def get_all(
        self,
        page: int = 1,
        page_size: int = 12,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        featured: Optional[bool] = None,
        active_only: bool = False,
        admin: bool = False,
    ) -> ProductListResponse:
        products, total, total_pages = self.repo.get_all(
            page=page,
            page_size=page_size,
            search=search,
            category_id=category_id,
            featured=featured,
            active_only=active_only,
        )
        return ProductListResponse(
            products=[self._to_response(p, admin=admin) for p in products],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    def get_by_slug(self, slug: str, admin: bool = False) -> ProductResponse:
        product = self.repo.get_by_slug(slug)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        return self._to_response(product, admin=admin)

    def get_featured(self, limit: int = 8) -> List[ProductResponse]:
        products = self.repo.get_featured(limit)
        return [self._to_response(p) for p in products]

    def get_related(self, product_id: int, category_id: int, limit: int = 4) -> List[ProductResponse]:
        products = self.repo.get_by_category(category_id, limit=limit, exclude_id=product_id)
        return [self._to_response(p) for p in products]

    def create(self, data: ProductCreate) -> ProductAdminResponse:
        # Validate category exists
        category = self.category_repo.get_by_id(data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category not found",
            )

        slug = slugify(data.name)
        if not slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid product name, cannot generate a valid URL slug.",
            )
            
        base_slug = slug
        counter = 1
        while self.repo.slug_exists(slug):
            slug = f"{base_slug}-{counter}"
            counter += 1

        product = Product(
            category_id=data.category_id,
            name=data.name,
            slug=slug,
            sku=data.sku,
            short_description=data.short_description,
            description=data.description,
            moq=data.moq,
            stock_status=data.stock_status,
            featured=data.featured,
            image=data.image,
            gallery_images=data.gallery_images or [],
            price=data.price,
            wholesale_price=data.wholesale_price,
            status=data.status,
        )
        product = self.repo.create(product)
        # Reload with category relationship
        product = self.repo.get_by_id(product.id)
        return self._to_response(product, admin=True)

    def update(self, product_id: int, data: ProductUpdate) -> ProductAdminResponse:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        if data.category_id is not None:
            category = self.category_repo.get_by_id(data.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category not found",
                )
            product.category_id = data.category_id

        if data.name is not None:
            product.name = data.name
            new_slug = slugify(data.name)
            if not new_slug:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid product name, cannot generate a valid URL slug.",
                )
            if new_slug != product.slug:
                base_slug = new_slug
                counter = 1
                while self.repo.slug_exists(new_slug, exclude_id=product_id):
                    new_slug = f"{base_slug}-{counter}"
                    counter += 1
                product.slug = new_slug

        update_fields = [
            "sku", "short_description", "description", "moq",
            "stock_status", "featured", "image", "gallery_images",
            "price", "wholesale_price", "status",
        ]
        for field in update_fields:
            value = getattr(data, field)
            if value is not None:
                setattr(product, field, value)

        product = self.repo.update(product)
        return self._to_response(product, admin=True)

    def delete(self, product_id: int) -> None:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        self.repo.delete(product)
