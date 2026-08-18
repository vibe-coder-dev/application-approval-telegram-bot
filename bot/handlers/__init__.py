# Handlers package
from .start import router as start_router
from .registration import router as registration_router
from .application import router as application_router
from .language import router as language_router
from .common import router as common_router

__all__ = [
    "start_router", "registration_router", "application_router", 
    "language_router", "common_router"
]
