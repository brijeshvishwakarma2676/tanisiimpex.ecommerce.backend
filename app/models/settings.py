"""
Site Settings model.
"""

from sqlalchemy import Column, Integer, String, Text, JSON

from app.database.base import Base


class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(200), nullable=False, default="Tanisi Impex")
    logo = Column(String(500), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    whatsapp_number = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    social_links = Column(JSON, nullable=True, default=dict)
