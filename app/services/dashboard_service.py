"""
Dashboard service - analytics and stats.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.product import Product
from app.models.category import Category
from app.models.inquiry import ProductInquiry


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_stats(self) -> dict:
        total_products = self.db.query(func.count(Product.id)).scalar() or 0
        total_categories = self.db.query(func.count(Category.id)).scalar() or 0
        total_inquiries = self.db.query(func.count(ProductInquiry.id)).scalar() or 0
        active_products = (
            self.db.query(func.count(Product.id))
            .filter(Product.status == True)
            .scalar()
            or 0
        )

        recent_inquiries = (
            self.db.query(ProductInquiry)
            .order_by(ProductInquiry.created_at.desc())
            .limit(5)
            .all()
        )
        
        return {
            "total_products": total_products,
            "total_categories": total_categories,
            "total_inquiries": total_inquiries,
            "active_products": active_products,
            "recent_inquiries": [
                {
                    "id": i.id,
                    "customer_name": i.customer_name,
                    "company_name": i.company_name,
                    "product_name": i.product.name if i.product else "Unknown",
                    "created_at": i.created_at.isoformat(),
                    "status": i.status
                } for i in recent_inquiries
            ]
        }
