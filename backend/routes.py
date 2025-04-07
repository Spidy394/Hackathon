from fastapi import APIRouter, HTTPException, status, Body, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from db import items_collection, containers_collection, logs_collection, placements_collection

# Custom Pydantic model with ObjectId support
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# Base Models with ObjectId handling
class MongoBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# Item Models
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int = Field(gt=0)
    category: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[Dict[str, float]] = None
    tags: Optional[List[str]] = []


class ItemCreate(ItemBase):
    pass


class ItemResponse(MongoBaseModel, ItemBase):
    pass


# Container Models
class ContainerBase(BaseModel):
    name: str
    capacity: Dict[str, float]
    location: Optional[str] = None
    status: str = "Active"
    description: Optional[str] = None


class ContainerCreate(ContainerBase):
    pass


class ContainerResponse(MongoBaseModel, ContainerBase):
    pass


# Placement Models
class PlacementBase(BaseModel):
    item_id: str
    container_id: str
    position: Optional[Dict[str, float]] = None
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    status: str = "Placed"


class PlacementCreate(PlacementBase):
    pass


class PlacementResponse(MongoBaseModel, PlacementBase):
    pass


# Log Models
class LogBase(BaseModel):
    action: str
    entity_type: str
    entity_id: str
    details: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    user_id: Optional[str] = None


class LogCreate(LogBase):
    pass


class LogResponse(MongoBaseModel, LogBase):
    pass


# Create API Router
api_router = APIRouter()


# ITEM ROUTES
@api_router.get("/items", response_model=List[ItemResponse], tags=["Items"])
async def get_all_items(
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=100)
):
    """Get all items with pagination"""
    items = list(items_collection.find().skip(skip).limit(limit))
    return items


@api_router.get("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
async def get_item(item_id: str):
    """Get a specific item by its ID"""
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item ID format")
    
    item = items_collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    return item


@api_router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def create_item(item: ItemCreate = Body(...)):
    """Create a new item"""
    item_dict = item.dict()
    result = items_collection.insert_one(item_dict)
    
    # Log the creation
    log_entry = {
        "action": "create",
        "entity_type": "item",
        "entity_id": str(result.inserted_id),
        "details": item_dict,
        "timestamp": datetime.now()
    }
    logs_collection.insert_one(log_entry)
    
    # Return the created item
    new_item = items_collection.find_one({"_id": result.inserted_id})
    return new_item


@api_router.put("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
async def update_item(item_id: str, item: ItemCreate = Body(...)):
    """Update an existing item"""
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item ID format")
    
    # Check if item exists
    existing_item = items_collection.find_one({"_id": ObjectId(item_id)})
    if not existing_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    # Update the item
    item_dict = item.dict()
    items_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": item_dict}
    )
    
    # Log the update
    log_entry = {
        "action": "update",
        "entity_type": "item",
        "entity_id": item_id,
        "details": item_dict,
        "timestamp": datetime.now()
    }
    logs_collection.insert_one(log_entry)
    
    # Return the updated item
    updated_item = items_collection.find_one({"_id": ObjectId(item_id)})
    return updated_item


@api_router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
async def delete_item(item_id: str):
    """Delete an item"""
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item ID format")
    
    # Check if item exists
    item = items_collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    # Delete the item
    items_collection.delete_one({"_id": ObjectId(item_id)})
    
    # Log the deletion
    log_entry = {
        "action": "delete",
        "entity_type": "item",
        "entity_id": item_id,
        "timestamp": datetime.now()
    }
    logs_collection.insert_one(log_entry)
    
    return None


# CONTAINER ROUTES
@api_router.get("/containers", response_model=List[ContainerResponse], tags=["Containers"])
async def get_all_containers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Get all containers with pagination"""
    containers = list(containers_collection.find().skip(skip).limit(limit))
    return containers


@api_router.get("/containers/{container_id}", response_model=ContainerResponse, tags=["Containers"])
async def get_container(container_id: str):
    """Get a specific container by its ID"""
    if not ObjectId.is_valid(container_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid container ID format")
    
    container = containers_collection.find_one({"_id": ObjectId(container_id)})
    if not container:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Container not found")
    
    return container


@api_router.post("/containers", response_model=ContainerResponse, status_code=status.HTTP_201_CREATED, tags=["Containers"])
async def create_container(container: ContainerCreate = Body(...)):
    """Create a new container"""
    container_dict = container.dict()
    result = containers_collection.insert_one(container_dict)
    
    # Log the creation
    log_entry = {
        "action": "create",
        "entity_type": "container",
        "entity_id": str(result.inserted_id),
        "details": container_dict,
        "timestamp": datetime.now()
    }
    logs_collection.insert_one(log_entry)
    
    # Return the created container
    new_container = containers_collection.find_one({"_id": result.inserted_id})
    return new_container


@api_router.put("/containers/{container_id}", response_model=ContainerResponse, tags=["Containers"])
async def update_container(container_id: str, container: ContainerCreate = Body(...)):
    """Update an existing container"""
    if not ObjectId.is_valid(container_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid container ID format")
    
    # Check if container exists
    existing_container = containers_collection.find_one({"_id": ObjectId(container_id)})
    if not existing_container:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Container not found")
    
    # Update the container
    container_dict = container.dict()
    containers_collection.update_one(
        {"_id": ObjectId(container_id)},
        {"$set": container_dict}
    )
    
    # Log the update
    log_entry = {
        "action": "update",
        "entity_type": "container",
        "entity_id": container_id,
        "details": container_dict,
        "timestamp": datetime.now()
    }
    logs_collection.insert_one(log_entry)
    
    # Return the updated container
    updated_container = containers_collection.find_one({"_id": ObjectId(container_id)})
    return updated_container


@api_router.delete("/containers/{container_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Containers"])
async def delete_container(container_id: str):
    """Delete a container"""
    if not ObjectId.is_valid(container_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid container ID format")
    
    # Check if container exists
    container = containers_collection.find_one({"_id": ObjectId(container_id)})
    if not container:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Container not found")
    
    # Delete the container
    containers_collection.delete_one({"_id": ObjectId(container_id)})
    
    # Log the deletion
    log_entry = {
        "action": "delete",
        "entity_type": "container",
        "entity_id": container_id,
        "timestamp": datetime.now()
    }
    logs_collection.insert_one(log_entry)
    
    return None


# PLACEMENT ROUTES
@api_router.get("/placements", response_model=List[PlacementResponse], tags=["Placements"])
async def get_all_placements(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Get all placements with pagination"""
    placements = list(placements_collection.find().skip(skip).limit(limit))
    return placements


@api_router.get("/placements/{placement_id}", response_model=PlacementResponse, tags=["Placements"])
async def get_placement(placement_id: str):
    """Get a specific placement by its ID"""
    if not ObjectId.is_valid(placement_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid placement ID format")
    
    placement = placements_collection.find_one({"_id": ObjectId(placement_id)})
    if not placement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Placement not found")
    
    return placement


@api_router.post("/placements", response_model=PlacementResponse, status_code=status.HTTP_201_CREATED, tags=["Placements"])
async def create_placement(placement: PlacementCreate = Body(...)):
    """Create a new placement"""
    # Validate that item and container exist
    if not ObjectId.is_valid(placement.item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item ID format")
    
    if not ObjectId.is_valid(placement.container_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid container ID format")
    
    item = items_collection.find_one({"_id": ObjectId(placement.item_id)})
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    container = containers_collection.find_one({"_id": ObjectId(placement.container_id)})
    if not container:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Container not found")
    
    # Create the placement
    placement_dict = placement.dict()
    result = placements_collection.insert_one(placement_dict)
    
    # Log the creation
    log_entry = {
        "action": "create",
        "entity_type": "placement",
        "entity_id": str(result.inserted_id),
        "details": placement_dict,
        "timestamp": datetime.now()
    }
    logs_collection.insert_one(log_entry)
    
    # Return the created placement
    new_placement = placements_collection.find_one({"_id": result.inserted_id})
    return new_placement


@api_router.put("/placements/{placement_id}", response_model=PlacementResponse, tags=["Placements"])
async def update_placement(placement_id: str, placement: PlacementCreate = Body(...)):
    """Update an existing placement"""
    if not ObjectId.is_valid(placement_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid placement ID format")
    
    # Check if placement exists
    existing_placement = placements_collection.find_one({"_id": ObjectId(placement_id)})
    if not existing_placement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Placement not found")
    
    # Validate that item and container exist
    if not ObjectId.is_valid(placement.item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item ID format")
    
    if not ObjectId.is_valid(placement.container_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid container ID format")
    
    item = items_collection.find_one({"_id": ObjectI
