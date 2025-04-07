from fastapi import APIRouter, Response
from db import placements_collection, items_collection, containers_collection
import csv
import io
from typing import List, Dict, Any

router = APIRouter()

@router.get("/api/export/arrangement", response_class=Response)
async def export_arrangement():
    """
    Export the current arrangement of items in containers as a CSV file
    
    Returns:
        CSV file with the current arrangement data
    """
    try:
        # Create a StringIO object to write CSV data
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header row
        writer.writerow(['containerId', 'itemId', 'x', 'y', 'z', 'rotation'])
        
        # Get all placements from the database
        placements = list(placements_collection.find({}, {"_id": 0}))
        
        # Write data rows
        for placement in placements:
            writer.writerow([
                placement.get('containerId', ''),
                placement.get('itemId', ''),
                placement.get('x', 0),
                placement.get('y', 0),
                placement.get('z', 0),
                placement.get('rotation', 0)
            ])
        
        # Get the CSV data as a string
        csv_data = output.getvalue()
        
        # Set response headers for CSV download
        headers = {
            'Content-Disposition': 'attachment; filename="arrangement_export.csv"',
            'Content-Type': 'text/csv'
        }
        
        # Return CSV response
        return Response(content=csv_data, headers=headers)
        
    except Exception as e:
        # In case of error, return JSON response with error message
        return Response(
            content=f"Error exporting arrangement: {str(e)}",
            media_type="text/plain",
            status_code=500
        )