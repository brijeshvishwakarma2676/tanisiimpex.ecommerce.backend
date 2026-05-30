"""
Site Settings schemas.
"""

from typing import Optional, Dict
from pydantic import BaseModel, EmailStr


class SettingsUpdate(BaseModel):
    company_name: Optional[str] = None
    logo: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    whatsapp_number: Optional[str] = None
    address: Optional[str] = None
    social_links: Optional[Dict[str, str]] = None


class SettingsResponse(BaseModel):
    id: int
    company_name: str
    logo: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    whatsapp_number: Optional[str] = None
    address: Optional[str] = None
    social_links: Optional[Dict[str, str]] = None

    class Config:
        from_attributes = True
