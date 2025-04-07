from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from models import (
    SimulateRequest, SimulateResponse, SimulationChanges,
    UsedItem, ExpiredItem, DepletedItem
)

def simulate_day_algorithm(
    request: SimulateRequest,
    all_items: List[Dict]
) -> SimulateResponse:
    """
    Algorithm to simulate the passage of time and item usage
    
    Args:
        request: SimulateRequest object with simulation parameters
        all_items: List of all items from the database
        
    Returns:
        SimulateResponse with changes after simulation
    """
    try:
        # Get the current date from the system
        current_date = datetime.now()
        
        # Calculate the new date based on numOfDays or toTimestamp
        if request.numOfDays is not None:
            new_date = current_date + timedelta(days=request.numOfDays)
            days_to_simulate = request.numOfDays
        elif request.toTimestamp is not None:
            try:
                # Handle different ISO formats with or without timezone info
                if 'Z' in request.toTimestamp:
                    new_date = datetime.fromisoformat(request.toTimestamp.replace('Z', '+00:00'))
                else:
                    new_date = datetime.fromisoformat(request.toTimestamp)
                # Calculate days between current date and target date
                days_to_simulate = max(1, (new_date - current_date).days)
            except ValueError as e:
                print(f"Error parsing timestamp: {e}")
                return SimulateResponse(
                    success=False,
                    newDate=current_date.isoformat(),
                    changes=SimulationChanges()
                )
        else:
            return SimulateResponse(
                success=False,
                newDate=current_date.isoformat(),
                changes=SimulationChanges()
            )
        
        if not all_items:
            print("No items found in database")
            return SimulateResponse(
                success=False,
                newDate=current_date.isoformat(),
                changes=SimulationChanges()
            )
        
        # Create lookup dictionaries for better performance
        item_by_id = {item["itemId"]: item.copy() for item in all_items}
        item_by_name = {item["name"]: item.copy() for item in all_items}
        
        # Create maps to keep track of items used per day
        items_to_use = {}
        
        # Process items to be used per day
        for item_usage in request.itemsToBeUsedPerDay:
            item_id = item_usage.itemId
            item_name = item_usage.name
            
            # Find the item either by ID or name
            item = None
            if item_id and item_id in item_by_id:
                item = item_by_id[item_id]
            elif item_name and item_name in item_by_name:
                item = item_by_name[item_name]
                # Update item_id to match the found item
                if item:
                    item_id = item["itemId"]
            
            if item and item_id:
                # Initialize current_usage field if it doesn't exist
                if "current_usage" not in item:
                    item["current_usage"] = 0
                items_to_use[item_id] = item
            else:
                # Item not found - log but continue with other items
                print(f"Item not found: ID={item_id}, Name={item_name}")
        
        if not items_to_use:
            print("No valid items to simulate usage for")
        
        # Track changes
        items_used = []
        items_expired = []
        items_depleted_today = []
        
        # Simulate each day
        for day in range(days_to_simulate):
            # Increment the current simulation date
            sim_date = current_date + timedelta(days=day + 1)
            sim_date_str = sim_date.strftime("%Y-%m-%d")
            
            # Process items used on this day
            for item_id, item in items_to_use.items():
                # Parse usage limit and simulate usage
                usage_limit = item.get("usageLimit", "N/A")
                
                if usage_limit != "N/A" and usage_limit.lower() != "unlimited":
                    # Parse usage limit (e.g., "30 uses" -> 30)
                    try:
                        if "uses" in usage_limit.lower():
                            # Extract the number from the usage limit
                            limit_value = int(usage_limit.lower().split("uses")[0].strip())
                            
                            # For simulation, we'll use a counter in-memory
                            current_usage = item["current_usage"] + 1
                            remaining_uses = max(0, limit_value - current_usage)
                            
                            # Update the item's usage in our in-memory state
                            item["current_usage"] = current_usage
                            
                            # For the final day, record the results
                            if day == days_to_simulate - 1:
                                if remaining_uses > 0:
                                    # Still has uses left
                                    items_used.append(UsedItem(
                                        itemId=item_id,
                                        name=item["name"],
                                        remainingUses=remaining_uses
                                    ))
                                else:
                                    # Depleted today (just ran out of uses)
                                    if current_usage == limit_value:
                                        items_depleted_today.append(DepletedItem(
                                            itemId=item_id,
                                            name=item["name"]
                                        ))
                    except (ValueError, TypeError) as e:
                        print(f"Error parsing usage limit for {item['name']}: {usage_limit} - {str(e)}")
                
                # Check for expiration on the final day
                if day == days_to_simulate - 1:
                    expiry_date = item.get("expiryDate", "N/A")
                    if expiry_date != "N/A" and expiry_date <= sim_date_str:
                        items_expired.append(ExpiredItem(
                            itemId=item_id,
                            name=item["name"]
                        ))
        
        # Create the response
        return SimulateResponse(
            success=True,
            newDate=new_date.isoformat(),
            changes=SimulationChanges(
                itemsUsed=items_used,
                itemsExpired=items_expired,
                itemsDepletedToday=items_depleted_today
            )
        )
        
    except Exception as e:
        print(f"Error simulating time: {str(e)}")
        import traceback
        traceback.print_exc()
        return SimulateResponse(
            success=False,
            newDate=datetime.now().isoformat(),
            changes=SimulationChanges()
        )