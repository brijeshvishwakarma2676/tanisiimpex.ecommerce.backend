"""
Category service - business logic.
"""

from typing import Tuple, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from slugify import slugify

from app.models.category import Category
from app.repositories.category_repo import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse


class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)

    def get_all(self, active_only: bool = False) -> Tuple[List[CategoryResponse], int]:
        categories, total = self.repo.get_all(active_only=active_only)
        result = []
        for cat in categories:
            product_count = self.repo.get_product_count(cat.id)
            resp = CategoryResponse(
                id=cat.id,
                name=cat.name,
                slug=cat.slug,
                image=cat.image,
                status=cat.status,
                created_at=cat.created_at,
                product_count=product_count,
            )
            result.append(resp)
        return result, total

    def get_by_slug(self, slug: str) -> CategoryResponse:
        category = self.repo.get_by_slug(slug)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
        product_count = self.repo.get_product_count(category.id)
        return CategoryResponse(
            id=category.id,
            name=category.name,
            slug=category.slug,
            image=category.image,
            status=category.status,
            created_at=category.created_at,
            product_count=product_count,
        )

    def create(self, data: CategoryCreate) -> CategoryResponse:
        slug = slugify(data.name)
        if not slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid category name, cannot generate a valid URL slug.",
            )
            
        # Ensure unique slug
        base_slug = slug
        counter = 1
        while self.repo.slug_exists(slug):
            slug = f"{base_slug}-{counter}"
            counter += 1

        category = Category(
            name=data.name,
            slug=slug,
            image=data.image,
            status=data.status,
        )
        category = self.repo.create(category)
        return CategoryResponse(
            id=category.id,
            name=category.name,
            slug=category.slug,
            image=category.image,
            status=category.status,
            created_at=category.created_at,
            product_count=0,
        )

    def update(self, category_id: int, data: CategoryUpdate) -> CategoryResponse:
        category = self.repo.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        if data.name is not None:
            category.name = data.name
            new_slug = slugify(data.name)
            if not new_slug:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid category name, cannot generate a valid URL slug.",
                )
            if new_slug != category.slug:
                base_slug = new_slug
                counter = 1
                while self.repo.slug_exists(new_slug, exclude_id=category_id):
                    new_slug = f"{base_slug}-{counter}"
                    counter += 1
                category.slug = new_slug

        if data.image is not None:
            category.image = data.image
        if data.status is not None:
            category.status = data.status

        category = self.repo.update(category)
        product_count = self.repo.get_product_count(category.id)
        return CategoryResponse(
            id=category.id,
            name=category.name,
            slug=category.slug,
            image=category.image,
            status=category.status,
            created_at=category.created_at,
            product_count=product_count,
        )

    def delete(self, category_id: int) -> None:
        category = self.repo.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
        product_count = self.repo.get_product_count(category_id)
        if product_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete category with {product_count} products. Remove products first.",
            )
        self.repo.delete(category)
