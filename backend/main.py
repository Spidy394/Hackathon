from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes import api_router

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

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Stellar Stash API is running"}

# Include all API routes
app.include_router(api_router)

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
