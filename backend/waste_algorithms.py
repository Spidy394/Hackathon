from typing import List, Optional, Dict, Any
from datetime import datetime
from models import (
    WasteItem, WasteResponse, Position, Coordinates,
    WasteReturnPlanResponse, WasteReturnStep, ReturnItem, ReturnManifest,
    RetrievalStep
)

def identify_waste_algorithm(items: List[Dict], containers: List[Dict]) -> WasteResponse:
    """
    Algorithm to identify waste items based on expiry date and usage limits
    
    Args:
        items: List of item objects from database
        containers: List of container objects from database
        
    Returns:
        WasteResponse object with identified waste items
    """
    try:
        # Get current date for expiry comparison
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Create a container lookup by ID
        container_map = {container["containerId"]: container for container in containers}
        
        # List to store waste items
        waste_items = []
        
        # Check each item for expiry or usage limit
        for item in items:
            # Default container and position if not found
            default_container_id = containers[0]["containerId"] if containers else "unknown"
            default_position = Position(
                startCoordinates=Coordinates(width=0.0, depth=0.0, height=0.0),
                endCoordinates=Coordinates(
                    width=float(item.get("width", 0)), 
                    depth=float(item.get("depth", 0)), 
                    height=float(item.get("height", 0))
                )
            )
            
            # Find container from preferred zone
            container_id = default_container_id
            for container in containers:
                if container["zone"] == item.get("preferredZone", ""):
                    container_id = container["containerId"]
                    break
            
            # Check if item is expired
            expiry_date = item.get("expiryDate", "N/A")
            if expiry_date != "N/A" and expiry_date < current_date:
                waste_items.append(WasteItem(
                    itemId=item["itemId"],
                    name=item["name"],
                    reason="Expired",
                    containerId=container_id,
                    position=default_position
                ))
                continue
            
            # Check if item is out of uses
            usage_limit = item.get("usageLimit", "N/A")
            if usage_limit != "N/A" and usage_limit.lower() != "unlimited":
                # Parse usage limit (e.g., "30 uses" -> 30)
                try:
                    if "uses" in usage_limit.lower():
                        limit_value = int(usage_limit.lower().split("uses")[0].strip())
                        # Simulate a random current usage between 0 and 120% of the limit
                        # In a real system, this would come from a usage counter in the database
                        # For this demo, we'll randomly mark some items as out of uses
                        import random
                        current_usage = random.randint(0, int(limit_value * 1.2))
                        
                        if current_usage >= limit_value:
                            waste_items.append(WasteItem(
                                itemId=item["itemId"],
                                name=item["name"],
                                reason="Out of Uses",
                                containerId=container_id,
                                position=default_position
                            ))
                except (ValueError, TypeError):
                    # Skip if usage limit cannot be parsed
                    pass
        
        return WasteResponse(success=True, wasteItems=waste_items)
    
    except Exception as e:
        print(f"Error in waste identification: {str(e)}")
        return WasteResponse(success=False, wasteItems=[])

def create_waste_return_plan_algorithm(
    waste_items: List[WasteItem], 
    undocking_container: Dict,
    undocking_date: str,
    max_weight: float,
    items_data: Dict[str, Dict]
) -> WasteReturnPlanResponse:
    """
    Algorithm to create a waste return plan based on identified waste items
    
    Args:
        waste_items: List of waste items to be returned
        undocking_container: Container object for undocking
        undocking_date: Date for undocking
        max_weight: Maximum weight constraint
        items_data: Dictionary of item data for weight calculations
        
    Returns:
        WasteReturnPlanResponse with return plan, retrieval steps, and manifest
    """
    try:
        if not waste_items:
            return WasteReturnPlanResponse(
                success=False,
                returnPlan=[],
                retrievalSteps=[],
                returnManifest=None
            )
        
        # Calculate container volume
        container_volume = undocking_container["width"] * undocking_container["depth"] * undocking_container["height"]
        
        # Select items to return based on maxWeight constraint
        return_items = []
        total_weight = 0
        total_volume = 0
        
        for waste_item in waste_items:
            item_data = items_data.get(waste_item.itemId)
            if not item_data:
                continue
                
            # Calculate item weight (simulated as 0.1-5kg based on volume)
            item_volume = item_data["width"] * item_data["depth"] * item_data["height"]
            item_weight = item_volume / 1000  # Simple formula: 1000 cubic cm = 1kg
            
            # Ensure minimum weight of 0.1kg and maximum of 5kg
            item_weight = max(0.1, min(5, item_weight))
            
            # Check if adding this item would exceed weight limit
            if total_weight + item_weight <= max_weight:
                return_items.append(ReturnItem(
                    itemId=waste_item.itemId,
                    name=waste_item.name,
                    reason=waste_item.reason
                ))
                total_weight += item_weight
                total_volume += item_volume
            
            # Stop if container is full (using a simple volume check)
            if total_volume >= container_volume * 0.9:  # Allow 90% fill capacity
                break
        
        # Generate return plan
        return_plan = []
        retrieval_steps = []
        step_counter = 1
        retrieval_step_counter = 1
        
        # Process each return item
        for i, return_item in enumerate(return_items):
            # Find the item in the waste items list
            waste_item = next((w for w in waste_items if w.itemId == return_item.itemId), None)
            if not waste_item:
                continue
                
            # Add return plan step
            return_plan.append(WasteReturnStep(
                step=step_counter,
                itemId=waste_item.itemId,
                itemName=waste_item.name,
                fromContainer=waste_item.containerId,
                toContainer=undocking_container["containerId"]
            ))
            step_counter += 1
            
            # Add retrieval steps
            # First, retrieve the item
            retrieval_steps.append(RetrievalStep(
                step=retrieval_step_counter,
                action="retrieve",
                itemId=waste_item.itemId,
                itemName=waste_item.name
            ))
            retrieval_step_counter += 1
            
            # If items are blocked, we need to set them aside
            if i < len(return_items) - 1:
                next_waste_item = next((w for w in waste_items if w.itemId == return_items[i+1].itemId), None)
                if next_waste_item and next_waste_item.containerId == waste_item.containerId:
                    # No need to move other items
                    pass
                else:
                    # We need to set aside the current item
                    retrieval_steps.append(RetrievalStep(
                        step=retrieval_step_counter,
                        action="setAside",
                        itemId=waste_item.itemId,
                        itemName=waste_item.name
                    ))
                    retrieval_step_counter += 1
        
        # Create return manifest
        return_manifest = ReturnManifest(
            undockingContainerId=undocking_container["containerId"],
            undockingDate=undocking_date,
            returnItems=return_items,
            totalVolume=total_volume,
            totalWeight=total_weight
        )
        
        return WasteReturnPlanResponse(
            success=True,
            returnPlan=return_plan,
            retrievalSteps=retrieval_steps,
            returnManifest=return_manifest
        )
        
    except Exception as e:
        print(f"Error creating waste return plan: {str(e)}")
        return WasteReturnPlanResponse(
            success=False,
            returnPlan=[],
            retrievalSteps=[],
            returnManifest=None
        )