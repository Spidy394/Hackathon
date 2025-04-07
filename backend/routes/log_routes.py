from fastapi import APIRouter
from typing import Optional
from models import LogResponse, LogRequest
from log_algorithms import get_logs_algorithm

router = APIRouter()

@router.get("/api/logs", response_model=LogResponse)
async def get_logs(
    startDate: str,
    endDate: str,
    itemId: Optional[str] = None,
    userId: Optional[str] = None,
    actionType: Optional[str] = None
):
    """
    Get logs filtered by date range and optional parameters.
    
    This endpoint uses the get_logs_algorithm from log_algorithms.py
    """
    return get_logs_algorithm(startDate, endDate, itemId, userId, actionType)

@router.post("/api/logs", response_model=LogResponse)
async def post_logs(request: LogRequest):
    """
    Get logs filtered by date range and optional parameters using POST method.
    
    This endpoint allows sending filtering criteria in the request body.
    """
    return get_logs_algorithm(
        request.startDate, 
        request.endDate, 
        request.itemId, 
        request.userId, 
        request.actionType
    )