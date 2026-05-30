"""
Product model.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, 
    ForeignKey, Numeric, JSON,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(250), unique=True, nullable=False, index=True)
    sku = Column(String(50), unique=True, nullable=True, index=True)
    short_description = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    moq = Column(Integer, default=1, nullable=False)
    stock_status = Column(String(20), default="in_stock", nullable=False)
    featured = Column(Boolean, default=False, nullable=False)
    image = Column(String(500), nullable=True)
    gallery_images = Column(JSON, nullable=True, default=list)
    # Hidden price fields (not shown publicly)
    price = Column(Numeric(10, 2), nullable=True)
    wholesale_price = Column(Numeric(10, 2), nullable=True)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    category = relationship("Category", back_populates="products")
    inquiries = relationship("ProductInquiry", back_populates="product", lazy="dynamic")
