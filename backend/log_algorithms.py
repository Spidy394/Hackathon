from typing import List, Optional
from db import logs_collection
from models import LogEntry, LogResponse

def get_logs_algorithm(
    startDate: str,
    endDate: str,
    itemId: Optional[str] = None,
    userId: Optional[str] = None,
    actionType: Optional[str] = None
) -> LogResponse:
    """
    Algorithm to retrieve and filter logs from the database
    
    Args:
        startDate: Start date in ISO format
        endDate: End date in ISO format
        itemId: Optional filter for specific item
        userId: Optional filter for specific user
        actionType: Optional filter for action type
    
    Returns:
        LogResponse object with filtered logs
    """
    try:
        # Create the base query with date range
        query = {
            "timestamp": {
                "$gte": startDate,
                "$lte": endDate
            }
        }
        
        # Add optional filters if provided
        if itemId:
            query["itemId"] = itemId
        
        if userId:
            query["userId"] = userId
        
        if actionType:
            # Validate action type
            valid_action_types = ["placement", "retrieval", "rearrangement", "disposal"]
            if actionType not in valid_action_types:
                return LogResponse(
                    success=False,
                    logs=[]
                )
            query["actionType"] = actionType
        
        # Fetch logs from the database
        logs_data = list(logs_collection.find(query, {"_id": 0}))
        
        # Convert database objects to LogEntry models
        logs = []
        for log in logs_data:
            log_entry = LogEntry(
                timestamp=log["timestamp"],
                userId=log["userId"],
                actionType=log["actionType"],
                itemId=log["itemId"],
                details=log.get("details")
            )
            logs.append(log_entry)
        
        return LogResponse(
            success=True,
            logs=logs
        )
    
    except Exception as e:
        print(f"Error retrieving logs: {str(e)}")
        return LogResponse(
            success=False,
            logs=[]
        )

def log_action(
    timestamp: str,
    userId: str,
    actionType: str,
    itemId: str,
    details: dict = None
) -> bool:
    """
    Helper function to log an action to the database
    
    Args:
        timestamp: Time when the action occurred
        userId: ID of the user who performed the action
        actionType: Type of action (placement, retrieval, etc.)
        itemId: ID of the item involved
        details: Additional details about the action
    
    Returns:
        Boolean indicating success or failure
    """
    try:
        log_entry = {
            "timestamp": timestamp,
            "userId": userId,
            "actionType": actionType,
            "itemId": itemId,
            "details": details or {}
        }
        logs_collection.insert_one(log_entry)
        return True
    except Exception as e:
        print(f"Error logging action: {str(e)}")
        return False