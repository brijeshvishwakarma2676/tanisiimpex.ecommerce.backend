"""
Dashboard routes - analytics.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.middleware.auth import get_current_admin
from app.schemas.response import success_response
from app.services.dashboard_service import DashboardService
from app.models.admin import Admin

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    service = DashboardService(db)
    stats = service.get_stats()
    return success_response("Dashboard stats fetched", stats)
