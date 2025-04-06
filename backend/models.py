from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from datetime import datetime
import uuid

class Coordinates(BaseModel):
    width: float
    depth: float
    height: float

class Position(BaseModel):
    startCoordinates: Coordinates
    endCoordinates: Coordinates

class Item(BaseModel):
    itemId: str
    name: str
    width: int
    depth: int
    height: int
    priority: int
    expiryDate: str
    usageLimit: str
    preferredZone: str

class Container(BaseModel):
    containerId: str
    zone: str
    width: int
    depth: int
    height: int

class PlacementRequest(BaseModel):
    items: List[Item]
    containers: List[Container]

class Placement(BaseModel):
    itemId: str
    containerId: str
    position: Position

class Rearrangement(BaseModel):
    step: int
    action: Literal["move", "remove", "place"]
    itemId: str
    fromContainer: Optional[str] = None
    fromPosition: Optional[Position] = None
    toContainer: Optional[str] = None
    toPosition: Optional[Position] = None

class PlacementResponse(BaseModel):
    success: bool
    placements: List[Placement]
    rearrangements: List[Rearrangement]

class RetrievalStep(BaseModel):
    step: int
    action: Literal["remove", "setAside", "retrieve", "placeBack"]
    itemId: str
    itemName: str

class ItemLocation(BaseModel):
    itemId: str
    name: str
    containerId: str
    zone: str
    position: Position

class SearchResponse(BaseModel):
    success: bool
    found: bool
    item: Optional[ItemLocation] = None
    retrievalSteps: List[RetrievalStep] = []

# Add this new model for the /api/place request
class PlaceItemRequest(BaseModel):
    itemId: str
    userId: str
    timestamp: str
    containerId: str
    position: Position

class WasteItem(BaseModel):
    itemId: str
    name: str
    reason: str  # "Expired", "Out of Uses"
    containerId: str
    position: Position

class WasteResponse(BaseModel):
    success: bool
    wasteItems: List[WasteItem] = []

class WasteReturnStep(BaseModel):
    step: int
    itemId: str
    itemName: str
    fromContainer: str
    toContainer: str

class ReturnItem(BaseModel):
    itemId: str
    name: str
    reason: str

class ReturnManifest(BaseModel):
    undockingContainerId: str
    undockingDate: str
    returnItems: List[ReturnItem]
    totalVolume: float
    totalWeight: float

class WasteReturnPlanRequest(BaseModel):
    undockingContainerId: str
    undockingDate: str
    maxWeight: float

class WasteReturnPlanResponse(BaseModel):
    success: bool
    returnPlan: List[WasteReturnStep] = []
    retrievalSteps: List[RetrievalStep] = []
    returnManifest: Optional[ReturnManifest] = None

class SimulateItemUsage(BaseModel):
    itemId: Optional[str] = None
    name: Optional[str] = None
    
    @validator('name')
    def either_id_or_name(cls, v, values):
        if not v and not values.get('itemId'):
            raise ValueError('Either itemId or name must be provided')
        return v

class SimulateRequest(BaseModel):
    numOfDays: Optional[int] = None
    toTimestamp: Optional[str] = None
    itemsToBeUsedPerDay: List[SimulateItemUsage]

class UsedItem(BaseModel):
    itemId: str
    name: str
    remainingUses: int

class ExpiredItem(BaseModel):
    itemId: str
    name: str

class DepletedItem(BaseModel):
    itemId: str
    name: str

class SimulationChanges(BaseModel):
    itemsUsed: List[UsedItem] = []
    itemsExpired: List[ExpiredItem] = []
    itemsDepletedToday: List[DepletedItem] = []

class SimulateResponse(BaseModel):
    success: bool
    newDate: str
    changes: SimulationChanges

class ImportError(BaseModel):
    row: int
    message: str

class ImportResponse(BaseModel):
    success: bool
    itemsImported: int
    errors: List[ImportError] = []

class LogDetails(BaseModel):
    fromContainer: Optional[str] = None
    toContainer: Optional[str] = None
    reason: Optional[str] = None

class LogEntry(BaseModel):
    timestamp: str
    userId: str
    actionType: str  # "placement", "retrieval", "rearrangement", "disposal"
    itemId: str
    details: Optional[LogDetails] = None

class LogRequest(BaseModel):
    startDate: str
    endDate: str
    itemId: Optional[str] = None
    userId: Optional[str] = None
    actionType: Optional[str] = None

class LogResponse(BaseModel):
    success: bool
    logs: List[LogEntry] = []

