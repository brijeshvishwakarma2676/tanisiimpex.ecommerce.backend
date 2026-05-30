"""
Inquiry repository - data access layer.
"""

import math
from typing import List, Optional, Tuple
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from app.models.inquiry import ProductInquiry
from app.models.product import Product


class InquiryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
    ) -> Tuple[List[ProductInquiry], int, int]:
        query = self.db.query(ProductInquiry).options(
            joinedload(ProductInquiry.product)
        )

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    ProductInquiry.customer_name.ilike(search_term),
                    ProductInquiry.email.ilike(search_term),
                    ProductInquiry.company_name.ilike(search_term),
                    ProductInquiry.phone.ilike(search_term),
                )
            )

        total = query.count()
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        offset = (page - 1) * page_size

        inquiries = (
            query.order_by(ProductInquiry.created_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return inquiries, total, total_pages

    def get_by_id(self, inquiry_id: int) -> Optional[ProductInquiry]:
        return (
            self.db.query(ProductInquiry)
            .options(joinedload(ProductInquiry.product))
            .filter(ProductInquiry.id == inquiry_id)
            .first()
        )

    def create(self, inquiry: ProductInquiry) -> ProductInquiry:
        self.db.add(inquiry)
        self.db.commit()
        self.db.refresh(inquiry)
        return inquiry

    def count(self) -> int:
        return self.db.query(func.count(ProductInquiry.id)).scalar()
