"""
Routes package initialization.
This module imports all API routes to make them available from the routes package.
"""

from fastapi import APIRouter

# Create the main API router
api_router = APIRouter()

# Import and include all route modules
from .item_routes import router as item_router
from .container_routes import router as container_router
from .placement_routes import router as placement_router
from .waste_routes import router as waste_router
from .log_routes import router as log_router
from .simulation_routes import router as simulation_router
from .import_routes import router as import_router

# Include all routers with appropriate prefixes
api_router.include_router(item_router, tags=["Items"])
api_router.include_router(container_router, tags=["Containers"])
api_router.include_router(placement_router, tags=["Placement"])
api_router.include_router(waste_router, tags=["Waste Management"])
api_router.include_router(log_router, tags=["Logs"])
api_router.include_router(simulation_router, tags=["Simulation"])
api_router.include_router(import_router, tags=["Import/Export"])