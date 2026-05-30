"""
Inquiry routes.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.rate_limit import limiter
from app.middleware.auth import get_current_admin
from app.schemas.inquiry import InquiryCreate
from app.schemas.response import success_response
from app.services.inquiry_service import InquiryService
from app.models.admin import Admin

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])


@router.post("")
@limiter.limit("3/minute")
def create_inquiry(request: Request, data: InquiryCreate, db: Session = Depends(get_db)):
    service = InquiryService(db)
    inquiry = service.create(data)
    return success_response("Inquiry submitted successfully", inquiry.model_dump())


@router.get("")
def list_inquiries(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    service = InquiryService(db)
    result = service.get_all(page=page, page_size=page_size, search=search)
    return success_response("Inquiries fetched", result.model_dump())


@router.get("/{inquiry_id}")
def get_inquiry(
    inquiry_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    service = InquiryService(db)
    inquiry = service.get_by_id(inquiry_id)
    return success_response("Inquiry fetched", inquiry.model_dump())
