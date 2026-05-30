"""
Product schemas.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    category_id: int
    name: str = Field(..., min_length=1, max_length=200)
    sku: Optional[str] = Field(None, max_length=50)
    short_description: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    moq: int = Field(1, ge=1)
    stock_status: str = Field("in_stock", pattern="^(in_stock|out_of_stock|limited)$")
    featured: bool = False
    image: Optional[str] = None
    gallery_images: Optional[List[str]] = []
    price: Optional[float] = None
    wholesale_price: Optional[float] = None
    status: bool = True


class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    sku: Optional[str] = Field(None, max_length=50)
    short_description: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    moq: Optional[int] = Field(None, ge=1)
    stock_status: Optional[str] = Field(None, pattern="^(in_stock|out_of_stock|limited)$")
    featured: Optional[bool] = None
    image: Optional[str] = None
    gallery_images: Optional[List[str]] = None
    price: Optional[float] = None
    wholesale_price: Optional[float] = None
    status: Optional[bool] = None


class ProductResponse(BaseModel):
    id: int
    category_id: int
    name: str
    slug: str
    sku: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    moq: int
    stock_status: str
    featured: bool
    image: Optional[str] = None
    gallery_images: Optional[List[str]] = []
    status: bool
    created_at: datetime
    updated_at: datetime
    category_name: Optional[str] = None

    class Config:
        from_attributes = True


class ProductAdminResponse(ProductResponse):
    """Admin version that includes hidden price fields."""
    price: Optional[float] = None
    wholesale_price: Optional[float] = None


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
