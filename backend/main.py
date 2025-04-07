from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes import api_router
from db import client as mongodb_client
import logging
import inspect

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastAPI application
app = FastAPI(title="stellar_stash")

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "http://frontend:4173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to verify MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    try:
        # Test MongoDB connection
        mongodb_client.admin.command('ping')
        logger.info("MongoDB connection successful")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")

# Debug endpoint to list all registered routes
@app.get("/debug/routes", tags=["Debug"])
async def list_routes():
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "name": route.name,
            "methods": [method for method in route.methods] if hasattr(route, "methods") else None
        })
    logger.info(f"Registered routes: {routes}")
    return routes

# Print detailed information about routes in api_router
logger.info("API Router routes before mounting:")
for route in api_router.routes:
    logger.info(f"Path: {route.path}, Name: {route.name}, Methods: {route.methods if hasattr(route, 'methods') else 'None'}")

# Check if routes already have /api prefix
has_api_prefix = any(route.path.startswith("/api/") for route in api_router.routes)

# Include router with appropriate prefix
if has_api_prefix:
    logger.info("Routes already have /api prefix, mounting router without additional prefix")
    app.include_router(api_router)
else:
    logger.info("Mounting router with /api prefix")
    app.include_router(api_router, prefix="/api")

# Print all registered routes after mounting
logger.info("All registered routes after mounting:")
for route in app.routes:
    logger.info(f"Path: {route.path}, Name: {route.name}, Methods: {route.methods if hasattr(route, 'methods') else 'None'}")

# Root endpoint
@app.get("/", tags=["Root"], summary="Root", 
         response_description="Welcome message")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Stellar Stash API is running"}

# Middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request path: {request.url.path}")
    response = await call_next(request)
    return response

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
