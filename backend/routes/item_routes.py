from fastapi import APIRouter, HTTPException, status, Body, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from bson import ObjectId
from db import items_collection, logs_collection
import json

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
    name: str = Field(..., min_length=1, description="Item name")
    description: Optional[str] = Field(None, description="Item description")
    quantity: int = Field(..., gt=0, description="Item quantity (must be positive)")
    category: Optional[str] = Field(None, description="Item category")
    weight: Optional[float] = Field(None, ge=0, description="Item weight in kg")
    dimensions: Optional[Dict[str, float]] = Field(None, description="Item dimensions")
    tags: Optional[List[str]] = Field(default_factory=list, description="Item tags")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or just whitespace')
        return v
        
    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be a positive integer')
        return v
        
    @validator('weight')
    def weight_must_be_non_negative(cls, v, values):
        if v is not None and v < 0:
            raise ValueError('Weight cannot be negative')
        return v
        
    class Config:
        schema_extra = {
            "example": {
                "name": "Example Item",
                "description": "This is an example item",
                "quantity": 10,
                "category": "Electronics",
                "weight": 1.5,
                "dimensions": {"length": 10.0, "width": 5.0, "height": 2.0},
                "tags": ["sample", "example"]
            }
        }


class ItemCreate(ItemBase):
    pass


class ItemResponse(MongoBaseModel, ItemBase):
    pass

# Helper function to convert MongoDB documents to JSON-serializable format
def serialize_mongodb_doc(doc):
    if doc is None:
        return None
    
    # Handle if doc is a list
    if isinstance(doc, list):
        return [serialize_mongodb_doc(item) for item in doc]
    
    # Convert document to dict if needed
    doc_dict = dict(doc)
    
    # Convert ObjectId to string
    if "_id" in doc_dict and isinstance(doc_dict["_id"], ObjectId):
        doc_dict["_id"] = str(doc_dict["_id"])
    
    # Handle nested documents
    for key, value in doc_dict.items():
        if isinstance(value, ObjectId):
            doc_dict[key] = str(value)
        elif isinstance(value, dict):
            doc_dict[key] = serialize_mongodb_doc(value)
        elif isinstance(value, list):
            doc_dict[key] = [
                serialize_mongodb_doc(item) if isinstance(item, (dict, list)) else 
                str(item) if isinstance(item, ObjectId) else item
                for item in value
            ]
    
    return doc_dict

# Convert MongoDB document to Pydantic model
def mongo_to_pydantic(doc, model_class):
    if doc is None:
        return None
    
    # If it's a list, process each item
    if isinstance(doc, list):
        return [mongo_to_pydantic(item, model_class) for item in doc]
    
    # Serialize the MongoDB doc first
    serialized = serialize_mongodb_doc(doc)
    
    # Create a Pydantic model instance
    return model_class(**serialized)


# Create router
router = APIRouter()

# Item routes
@router.get("/items", response_model=List[ItemResponse], tags=["Items"])
async def get_all_items(
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=100)
):
    """
    Get all items with pagination
    
    - **skip**: Number of items to skip
    - **limit**: Maximum number of items to return
    
    Returns a list of items
    """
    items = list(items_collection.find().skip(skip).limit(limit))
    return mongo_to_pydantic(items, ItemResponse)


@router.get("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
async def get_item(item_id: str):
    """
    Get a specific item by its ID
    
    - **item_id**: The ID of the item to retrieve
    
    Returns the item if found, 404 if not found
    """
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item ID format")
    
    item = items_collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    return mongo_to_pydantic(item, ItemResponse)


@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def create_item(item: ItemCreate = Body(..., example={
    "name": "New Item",
    "description": "A new item description",
    "quantity": 5,
    "category": "General",
    "weight": 1.2
})):
    """
    Create a new item
    
    - **item**: Item data to create
    
    Required fields:
    - name: String (non-empty)
    - quantity: Integer (positive)
    
    Optional fields:
    - description: String
    - category: String
    - weight: Float (non-negative)
    - dimensions: Dictionary of measurements
    - tags: List of strings
    
    Returns the created item
    """
    try:
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
        return mongo_to_pydantic(new_item, ItemResponse)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.put("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
async def update_item(
    item_id: str, 
    item: ItemCreate = Body(..., example={
        "name": "Updated Item",
        "description": "Updated description",
        "quantity": 10,
        "category": "Updated Category",
        "weight": 2.5
    })
):
    """
    Update an existing item
    
    - **item_id**: The ID of the item to update
    - **item**: New item data
    
    Required fields:
    - name: String (non-empty)
    - quantity: Integer (positive)
    
    Optional fields:
    - description: String
    - category: String
    - weight: Float (non-negative)
    - dimensions: Dictionary of measurements
    - tags: List of strings
    
    Returns the updated item
    """
    try:
        if not ObjectId.is_valid(item_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item ID format")
        
        # Check if item exists
        existing_item = items_collection.find_one({"_id": ObjectId(item_id)})
        if not existing_item:
            raise HTTPException(status_code=status.HTTP
