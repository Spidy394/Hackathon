from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import items_collection, containers_collection

app = FastAPI()

origins = [
    "http://localhost:5173",  # frontend dev server (vite)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/items")
async def get_items():
    items = list(items_collection.find({}, {"_id": 0}))
    return {"items": items}

@app.get("/api/containers")
async def get_containers():
    containers = list(containers_collection.find({}, {"_id": 0}))
    return {"containers": containers}
