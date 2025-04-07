from fastapi import APIRouter
from db import items_collection, containers_collection
from models import WasteResponse, WasteReturnPlanRequest, WasteReturnPlanResponse
from waste_algorithms import identify_waste_algorithm, create_waste_return_plan_algorithm
from log_algorithms import log_action

router = APIRouter()

@router.get("/api/waste/identify", response_model=WasteResponse)
async def identify_waste():
    """Identify items that should be disposed of (expired or out of uses)"""
    try:
        # Get all items and containers
        items = list(items_collection.find({}, {"_id": 0}))
        if not items:
            print("No items found in database for waste identification")
            return WasteResponse(success=True, wasteItems=[])
            
        containers = list(containers_collection.find({}, {"_id": 0}))
        if not containers:
            print("No containers found in database for waste identification")
            # We still need containers for the algorithm to work properly
            # Return an empty response but inform about the issue
            return WasteResponse(success=True, wasteItems=[])
        
        # Log the items and containers count for debugging
        print(f"Checking {len(items)} items and {len(containers)} containers for waste identification")
        
        # Use the waste identification algorithm
        result = identify_waste_algorithm(items, containers)
        
        # Log the waste items count
        if result.success:
            print(f"Identified {len(result.wasteItems)} waste items")
        else:
            print("Waste identification failed")
            
        return result
    
    except Exception as e:
        error_message = f"Error in waste identification: {str(e)}"
        print(error_message)
        
        # Return a more informative error response
        return WasteResponse(
            success=False, 
            wasteItems=[]
        )

@router.post("/api/waste/return-plan", response_model=WasteReturnPlanResponse)
async def create_waste_return_plan(request: WasteReturnPlanRequest):
    """Create a plan for returning waste items"""
    try:
        # First identify waste items
        waste_response = await identify_waste()
        if not waste_response.success or len(waste_response.wasteItems) == 0:
            return WasteReturnPlanResponse(
                success=False,
                returnPlan=[],
                retrievalSteps=[],
                returnManifest=None
            )
        
        # Get container information
        undocking_container = containers_collection.find_one({"containerId": request.undockingContainerId}, {"_id": 0})
        if not undocking_container:
            return WasteReturnPlanResponse(
                success=False,
                returnPlan=[],
                retrievalSteps=[],
                returnManifest=None
            )
        
        # Get all items from database for weight and volume calculations
        items_data = {item["itemId"]: item for item in items_collection.find({}, {"_id": 0})}
        
        # Use the return plan algorithm
        return create_waste_return_plan_algorithm(
            waste_items=waste_response.wasteItems,
            undocking_container=undocking_container,
            undocking_date=request.undockingDate,
            max_weight=request.maxWeight,
            items_data=items_data
        )
        
    except Exception as e:
        print(f"Error creating waste return plan: {str(e)}")
        return WasteReturnPlanResponse(
            success=False,
            returnPlan=[],
            retrievalSteps=[],
            returnManifest=None
        )

@router.post("/api/waste/complete-undocking")
async def complete_undocking(request: dict):
    """Complete the undocking process and log disposal of waste items"""
    try:
        # Extract request data
        undocking_container_id = request.get("undockingContainerId")
        timestamp = request.get("timestamp")
        userId = request.get("userId", "system")  # Default to "system" if no user ID provided
        
        if not undocking_container_id or not timestamp:
            return {"success": False, "itemsRemoved": 0}
        
        # First, check if the container exists
        container = containers_collection.find_one({"containerId": undocking_container_id}, {"_id": 0})
        if not container:
            return {"success": False, "itemsRemoved": 0, "message": "Container not found"}
        
        # Then identify waste items
        waste_response = await identify_waste()
        
        if not waste_response.success or len(waste_response.wasteItems) == 0:
            return {"success": True, "itemsRemoved": 0}
        
        # Get IDs of all waste items
        waste_item_ids = [item.itemId for item in waste_response.wasteItems]
        
        # Count of items to be removed
        items_removed = len(waste_item_ids)
        
        if items_removed == 0:
            return {"success": True, "itemsRemoved": 0}
        
        # Log the undocking operation
        print(f"Completed undocking of container {undocking_container_id} at {timestamp}")
        print(f"Removed {items_removed} waste items: {', '.join(waste_item_ids)}")
        
        # Log each waste item disposal
        for waste_item in waste_response.wasteItems:
            log_action(
                timestamp=timestamp,
                userId=userId,
                actionType="disposal",
                itemId=waste_item.itemId,
                details={
                    "fromContainer": waste_item.containerId,
                    "toContainer": undocking_container_id,
                    "reason": waste_item.reason
                }
            )
        
        return {
            "success": True,
            "itemsRemoved": items_removed
        }
    
    except Exception as e:
        print(f"Error completing undocking: {str(e)}")
        return {"success": False, "itemsRemoved": 0, "message": str(e)}