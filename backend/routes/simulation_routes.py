from fastapi import APIRouter
from db import items_collection
from models import SimulateRequest, SimulateResponse, SimulationChanges
from simulation_algorithms import simulate_day_algorithm
from datetime import datetime

router = APIRouter()

@router.post("/api/simulate/day", response_model=SimulateResponse)
async def simulate_day(request: SimulateRequest):
    """Simulate the passage of time and item usage"""
    try:
        # Get all items from the database
        all_items = list(items_collection.find({}, {"_id": 0}))
        
        # Use the simulation algorithm
        return simulate_day_algorithm(request, all_items)
        
    except Exception as e:
        print(f"Error simulating time: {str(e)}")
        import traceback
        traceback.print_exc()
        return SimulateResponse(
            success=False,
            newDate=datetime.now().isoformat(),
            changes=SimulationChanges()
        )