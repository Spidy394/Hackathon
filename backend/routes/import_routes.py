from fastapi import APIRouter, File, UploadFile
from db import items_collection, containers_collection
from models import ImportResponse, ImportError
from import_algorithms import import_items_algorithm, import_containers_algorithm

router = APIRouter()

@router.post("/api/import/items", response_model=ImportResponse)
async def import_items(file: UploadFile = File(...)):
    """Import items from a CSV file"""
    try:
        # Check if the file is a CSV
        if not file.filename.endswith('.csv'):
            return ImportResponse(
                success=False,
                itemsImported=0,
                errors=[ImportError(row=0, message="Uploaded file must be a CSV file")]
            )
        
        # Read the file content and decode it
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Use the import algorithm to parse the CSV
        import_response, parsed_items = import_items_algorithm(content_str)
        
        # If import was successful, update or insert items in the database
        if import_response.success and parsed_items:
            for item in parsed_items:
                # Check if item with this ID already exists
                existing_item = items_collection.find_one({"itemId": item["itemId"]})
                if existing_item:
                    # Update existing item
                    items_collection.update_one(
                        {"itemId": item["itemId"]},
                        {"$set": item}
                    )
                else:
                    # Insert new item
                    items_collection.insert_one(item)
                    
        return import_response
        
    except Exception as e:
        return ImportResponse(
            success=False,
            itemsImported=0,
            errors=[ImportError(row=0, message=f"Error processing file: {str(e)}")]
        )

@router.post("/api/import/containers", response_model=ImportResponse)
async def import_containers(file: UploadFile = File(...)):
    """Import containers from a CSV file"""
    try:
        # Check if the file is a CSV
        if not file.filename.endswith('.csv'):
            return ImportResponse(
                success=False,
                itemsImported=0,
                errors=[ImportError(row=0, message="Uploaded file must be a CSV file")]
            )
        
        # Read the file content and decode it
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Use the import algorithm to parse the CSV
        import_response, parsed_containers = import_containers_algorithm(content_str)
        
        # If import was successful, update or insert containers in the database
        if import_response.success and parsed_containers:
            for container in parsed_containers:
                # Check if container with this ID already exists
                existing_container = containers_collection.find_one({"containerId": container["containerId"]})
                if existing_container:
                    # Update existing container
                    containers_collection.update_one(
                        {"containerId": container["containerId"]},
                        {"$set": container}
                    )
                else:
                    # Insert new container
                    containers_collection.insert_one(container)
                    
        return import_response
        
    except Exception as e:
        return ImportResponse(
            success=False,
            itemsImported=0,
            errors=[ImportError(row=0, message=f"Error processing file: {str(e)}")]
        )