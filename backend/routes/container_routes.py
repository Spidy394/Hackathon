from fastapi import APIRouter
from db import containers_collection
from typing import Dict, List

router = APIRouter()

@router.get("/api/containers")
async def get_containers():
    """Get all containers from the database"""
    containers = list(containers_collection.find({}, {"_id": 0}))
    return {"containers": containers}