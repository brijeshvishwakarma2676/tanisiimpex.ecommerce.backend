"""
Seed script - creates initial admin user and default settings.
Run: python seed.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database.connection import SessionLocal
from app.database.base import Base
from app.database.connection import engine
from app.models.admin import Admin
from app.models.settings import SiteSettings
from app.core.security import hash_password

# Import all models
from app.models import *

# Create tables
Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()

    try:
        # Create default admin
        existing = db.query(Admin).filter(Admin.email == "admin@tanisiimpex.com").first()
        if not existing:
            admin = Admin(
                full_name="Admin",
                email="admin@tanisiimpex.com",
                password_hash=hash_password("Admin@123"),
                is_active=True,
            )
            db.add(admin)
            print("✅ Default admin created: admin@tanisiimpex.com / Admin@123")
        else:
            print("ℹ️  Admin already exists")

        # Create default settings
        settings = db.query(SiteSettings).first()
        if not settings:
            settings = SiteSettings(
                company_name="Tanisi Impex",
                email="info@tanisiimpex.com",
                phone="+91 9876543210",
                whatsapp_number="+919876543210",
                address="Mumbai, Maharashtra, India",
                social_links={
                    "facebook": "https://facebook.com/tanisiimpex",
                    "instagram": "https://instagram.com/tanisiimpex",
                    "linkedin": "https://linkedin.com/company/tanisiimpex",
                },
            )
            db.add(settings)
            print("✅ Default site settings created")
        else:
            print("ℹ️  Site settings already exist")

        db.commit()
        print("\n🎉 Seed completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
