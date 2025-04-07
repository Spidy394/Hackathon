from fastapi import APIRouter
from typing import Optional
from models import LogResponse
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