from fastapi import APIRouter, HTTPException
from typing import Optional
from db import items_collection, containers_collection
from models import PlacementRequest, PlacementResponse, SearchResponse, PlaceItemRequest
from algorithms import calculate_placement, search_item_algorithm
from log_algorithms import log_action

router = APIRouter()

@router.post("/api/placement", response_model=PlacementResponse)
async def create_placement(request: PlacementRequest):
    """Calculate optimal placement for items in containers"""
    try:
        result = calculate_placement(request.items, request.containers)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing placement: {str(e)}")

@router.get("/api/search", response_model=SearchResponse)
async def search_item(
    itemId: str = None, 
    itemName: str = None,
    userId: str = None
):
    """Search for an item by ID or name and provide retrieval steps"""
    if not itemId and not itemName:
        raise HTTPException(status_code=400, detail="Either itemId or itemName must be provided")
    
    query = {}
    if itemId:
        query["itemId"] = itemId
    elif itemName:
        query["name"] = itemName
    
    item_data = items_collection.find_one(query, {"_id": 0})
    
    if not item_data:
        return SearchResponse(success=True, found=False)
    
    container_query = {"zone": item_data.get("preferredZone", "")}
    container = containers_collection.find_one(container_query, {"_id": 0})
    
    if not container:
        container = containers_collection.find_one({}, {"_id": 0})
    
    if container and container["zone"] == "Airlock":
        blocker_item = items_collection.find_one(
            {"preferredZone": "Airlock", "itemId": {"$ne": item_data["itemId"]}},
            {"_id": 0}
        )
        if blocker_item:
            item_data["blocker_item"] = blocker_item
    
    print(f"Item {item_data['itemId']} - {item_data['name']} has been used once.")
    
    if userId:
        print(f"User {userId} retrieved item {item_data['itemId']}.")
    
    return search_item_algorithm(item_data, container)

@router.post("/api/retrieve")
async def retrieve_item(
    itemId: str,
    userId: str,
    timestamp: str
):
    """Record the retrieval of an item"""
    try:
        item = items_collection.find_one({"itemId": itemId}, {"_id": 0})
        
        if not item:
            return {"success": False, "message": "Item not found"}
        
        print(f"Item {itemId} retrieved by user {userId} at {timestamp}")
        
        # Log the retrieval action
        log_action(
            timestamp=timestamp,
            userId=userId,
            actionType="retrieval",
            itemId=itemId,
            details={"reason": "User retrieval request"}
        )
        
        return {"success": True}
        
    except Exception as e:
        return {"success": False, "message": str(e)}

@router.post("/api/place")
async def place_item(request: PlaceItemRequest):
    """Record the placement of an item in a container"""
    try:
        # First check if the container exists
        container = containers_collection.find_one({"containerId": request.containerId}, {"_id": 0})
        if not container:
            return {"success": False, "message": "Container not found"}
        
        # Then check if the item exists
        item = items_collection.find_one({"itemId": request.itemId}, {"_id": 0})
        if not item:
            return {"success": False, "message": "Item not found"}
        
        # Log the placement action
        print(f"Item {request.itemId} placed in container {request.containerId} by user {request.userId} at {request.timestamp}")
        print(f"Position: {request.position.dict()}")
        
        # Log the action
        log_action(
            timestamp=request.timestamp,
            userId=request.userId,
            actionType="placement",
            itemId=request.itemId,
            details={"toContainer": request.containerId}
        )
        
        return {"success": True}
        
    except Exception as e:
        return {"success": False, "message": str(e)}