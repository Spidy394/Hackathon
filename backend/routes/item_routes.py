from fastapi import APIRouter, HTTPException
from db import items_collection
from typing import Dict, List

router = APIRouter()

@router.get("/api/items")
async def get_items():
    """Get all items from the database"""
    items = list(items_collection.find({}, {"_id": 0}))
    return {"items": items}