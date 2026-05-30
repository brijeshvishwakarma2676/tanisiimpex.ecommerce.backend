"""
Settings routes.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.middleware.auth import get_current_admin
from app.schemas.settings import SettingsUpdate, SettingsResponse
from app.schemas.response import success_response
from app.repositories.settings_repo import SettingsRepository
from app.models.settings import SiteSettings
from app.models.admin import Admin

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("")
def get_settings(db: Session = Depends(get_db)):
    repo = SettingsRepository(db)
    settings = repo.get()
    if not settings:
        # Create default settings
        settings = SiteSettings(company_name="Tanisi Impex")
        settings = repo.create(settings)
    return success_response(
        "Settings fetched",
        SettingsResponse.model_validate(settings).model_dump(),
    )


@router.put("")
def update_settings(
    data: SettingsUpdate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    repo = SettingsRepository(db)
    settings = repo.get()
    if not settings:
        settings = SiteSettings(company_name="Tanisi Impex")
        settings = repo.create(settings)

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(settings, field, value)

    settings = repo.update(settings)
    return success_response(
        "Settings updated",
        SettingsResponse.model_validate(settings).model_dump(),
    )
