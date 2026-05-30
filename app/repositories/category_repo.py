"""
Category repository - data access layer.
"""

from typing import List, Optional, Tuple
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, active_only: bool = False) -> Tuple[List[Category], int]:
        query = self.db.query(Category)
        if active_only:
            query = query.filter(Category.status == True)
        query = query.order_by(Category.created_at.desc())
        total = query.count()
        categories = query.all()
        return categories, total

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_by_slug(self, slug: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.slug == slug).first()

    def create(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category: Category) -> Category:
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category) -> None:
        self.db.delete(category)
        self.db.commit()

    def get_product_count(self, category_id: int) -> int:
        return (
            self.db.query(func.count(Product.id))
            .filter(Product.category_id == category_id)
            .scalar()
        )

    def slug_exists(self, slug: str, exclude_id: Optional[int] = None) -> bool:
        query = self.db.query(Category).filter(Category.slug == slug)
        if exclude_id:
            query = query.filter(Category.id != exclude_id)
        return query.first() is not None
