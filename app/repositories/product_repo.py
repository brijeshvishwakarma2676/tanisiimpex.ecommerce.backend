"""
Product repository - data access layer.
"""

import math
from typing import List, Optional, Tuple
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from app.models.product import Product
from app.models.category import Category


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        page: int = 1,
        page_size: int = 12,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        featured: Optional[bool] = None,
        active_only: bool = False,
    ) -> Tuple[List[Product], int, int]:
        """Get paginated products with filters. Returns (products, total, total_pages)."""
        query = self.db.query(Product).options(joinedload(Product.category))

        if active_only:
            query = query.filter(Product.status == True)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.short_description.ilike(search_term),
                    Product.sku.ilike(search_term),
                )
            )

        if category_id:
            query = query.filter(Product.category_id == category_id)

        if featured is not None:
            query = query.filter(Product.featured == featured)

        total = query.count()
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        offset = (page - 1) * page_size

        products = (
            query.order_by(Product.created_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return products, total, total_pages

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id == product_id)
            .first()
        )

    def get_by_slug(self, slug: str) -> Optional[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.slug == slug)
            .first()
        )

    def get_featured(self, limit: int = 8) -> List[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.featured == True, Product.status == True)
            .order_by(Product.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_by_category(self, category_id: int, limit: int = 4, exclude_id: Optional[int] = None) -> List[Product]:
        """Get related products in the same category."""
        query = (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.category_id == category_id, Product.status == True)
        )
        if exclude_id:
            query = query.filter(Product.id != exclude_id)
        return query.order_by(Product.created_at.desc()).limit(limit).all()

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product) -> Product:
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()

    def slug_exists(self, slug: str, exclude_id: Optional[int] = None) -> bool:
        query = self.db.query(Product).filter(Product.slug == slug)
        if exclude_id:
            query = query.filter(Product.id != exclude_id)
        return query.first() is not None

    def count(self) -> int:
        return self.db.query(func.count(Product.id)).scalar()
