from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    id: str
    name: str
    width: int
    depth: int
    height: int
    mass: float
    priority: int
    expiryDate: str
    usageLimit: str
    preferredZone: str

class Container(BaseModel):
    zone: str
    containerId: str
    width: int
    depth: int
    height: int
