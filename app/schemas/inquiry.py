"""
Inquiry schemas.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class InquiryCreate(BaseModel):
    product_id: int
    customer_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=7, max_length=20)
    company_name: Optional[str] = Field(None, max_length=200)
    quantity_required: int = Field(..., ge=1)
    message: Optional[str] = None


class InquiryResponse(BaseModel):
    id: int
    product_id: int
    customer_name: str
    email: str
    phone: str
    company_name: Optional[str] = None
    quantity_required: int
    message: Optional[str] = None
    created_at: datetime
    product_name: Optional[str] = None

    class Config:
        from_attributes = True


class InquiryListResponse(BaseModel):
    inquiries: list[InquiryResponse]
    total: int
    page: int
    page_size: int
