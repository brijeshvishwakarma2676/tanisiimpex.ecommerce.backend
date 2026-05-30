"""
Standardized API response wrapper.
"""

from typing import Any, Optional
from pydantic import BaseModel


class ApiResponse(BaseModel):
    """Standard API response format."""
    success: bool
    message: str
    data: Optional[Any] = None


def success_response(message: str, data: Any = None) -> dict:
    """Create a success response."""
    return {"success": True, "message": message, "data": data}


def error_response(message: str, data: Any = None) -> dict:
    """Create an error response."""
    return {"success": False, "message": message, "data": data}
