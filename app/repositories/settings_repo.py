"""
Settings repository - data access layer.
"""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.settings import SiteSettings


class SettingsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self) -> Optional[SiteSettings]:
        """Get the singleton site settings row."""
        return self.db.query(SiteSettings).first()

    def create(self, settings: SiteSettings) -> SiteSettings:
        self.db.add(settings)
        self.db.commit()
        self.db.refresh(settings)
        return settings

    def update(self, settings: SiteSettings) -> SiteSettings:
        self.db.commit()
        self.db.refresh(settings)
        return settings
