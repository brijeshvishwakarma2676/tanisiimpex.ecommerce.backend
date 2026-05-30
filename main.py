"""
Tanisi Impex - B2B Wholesale Ecommerce Platform
Main Application Entry Point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.rate_limit import limiter
from app.database.base import Base
from app.database.connection import engine
from app.api import auth, categories, products, inquiries, settings as settings_routes, upload, dashboard

# Import all models so they are registered with Base
from app.models import Admin, Category, Product, ProductInquiry, SiteSettings

import logging
from app.database.connection import SessionLocal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Tanisi Impex API",
    description="B2B Wholesale Ecommerce Platform API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(inquiries.router, prefix="/api")
app.include_router(settings_routes.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.method} {request.url}", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error"},
    )


from sqlalchemy import text

@app.get("/api/health")
def health_check():
    db_status = "disconnected"
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error("Health check DB connection failed", exc_info=e)
    finally:
        try:
            db.close()
        except:
            pass
            
    return {
        "success": True, 
        "message": "API is running", 
        "data": {
            "version": "1.0.0",
            "database": db_status
        }
    }
