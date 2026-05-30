"""
Inquiry service - business logic.
"""

from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.inquiry import ProductInquiry
from app.repositories.inquiry_repo import InquiryRepository
from app.repositories.product_repo import ProductRepository
from app.schemas.inquiry import InquiryCreate, InquiryResponse, InquiryListResponse
from app.core.email import send_inquiry_admin_notification, send_inquiry_customer_confirmation


class InquiryService:
    def __init__(self, db: Session):
        self.repo = InquiryRepository(db)
        self.product_repo = ProductRepository(db)

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
    ) -> InquiryListResponse:
        inquiries, total, total_pages = self.repo.get_all(
            page=page, page_size=page_size, search=search
        )
        return InquiryListResponse(
            inquiries=[
                InquiryResponse(
                    id=inq.id,
                    product_id=inq.product_id,
                    customer_name=inq.customer_name,
                    email=inq.email,
                    phone=inq.phone,
                    company_name=inq.company_name,
                    quantity_required=inq.quantity_required,
                    message=inq.message,
                    created_at=inq.created_at,
                    product_name=inq.product.name if inq.product else None,
                )
                for inq in inquiries
            ],
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_by_id(self, inquiry_id: int) -> InquiryResponse:
        inquiry = self.repo.get_by_id(inquiry_id)
        if not inquiry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inquiry not found",
            )
        return InquiryResponse(
            id=inquiry.id,
            product_id=inquiry.product_id,
            customer_name=inquiry.customer_name,
            email=inquiry.email,
            phone=inquiry.phone,
            company_name=inquiry.company_name,
            quantity_required=inquiry.quantity_required,
            message=inquiry.message,
            created_at=inquiry.created_at,
            product_name=inquiry.product.name if inquiry.product else None,
        )

    def create(self, data: InquiryCreate) -> InquiryResponse:
        # Validate product exists
        product = self.product_repo.get_by_id(data.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product not found",
            )

        inquiry = ProductInquiry(
            product_id=data.product_id,
            customer_name=data.customer_name,
            email=data.email,
            phone=data.phone,
            company_name=data.company_name,
            quantity_required=data.quantity_required,
            message=data.message,
        )
        inquiry = self.repo.create(inquiry)

        # Send email notifications (non-blocking, don't fail on email errors)
        try:
            email_data = {
                "product_name": product.name,
                "customer_name": data.customer_name,
                "email": data.email,
                "phone": data.phone,
                "company_name": data.company_name or "N/A",
                "quantity_required": data.quantity_required,
                "message": data.message or "No message provided",
            }
            send_inquiry_admin_notification(email_data)
            send_inquiry_customer_confirmation(email_data)
        except Exception as e:
            print(f"Email notification failed: {e}")

        return InquiryResponse(
            id=inquiry.id,
            product_id=inquiry.product_id,
            customer_name=inquiry.customer_name,
            email=inquiry.email,
            phone=inquiry.phone,
            company_name=inquiry.company_name,
            quantity_required=inquiry.quantity_required,
            message=inquiry.message,
            created_at=inquiry.created_at,
            product_name=product.name,
        )
