"""
Auth routes.
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.rate_limit import limiter
from app.middleware.auth import get_current_admin
from app.schemas.auth import LoginRequest, RefreshRequest, AdminResponse
from app.schemas.response import success_response
from app.services.auth_service import AuthService
from app.models.admin import Admin

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, credentials: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    tokens = service.login(credentials)
    return success_response("Login successful", tokens.model_dump())


@router.post("/refresh")
@limiter.limit("10/minute")
def refresh_token(request: Request, body: RefreshRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    tokens = service.refresh_token(body.refresh_token)
    return success_response("Token refreshed", tokens.model_dump())


@router.get("/me")
def get_me(admin: Admin = Depends(get_current_admin)):
    return success_response(
        "Admin fetched",
        AdminResponse.model_validate(admin).model_dump(),
    )
