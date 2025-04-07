import csv
import io
from typing import List, Dict, Any, Tuple
from models import ImportError, ImportResponse

def import_items_algorithm(content_str: str) -> Tuple[ImportResponse, List[Dict[str, Any]]]:
    """
    Algorithm to import items from a CSV file
    
    Args:
        content_str: CSV content as a string
        
    Returns:
        ImportResponse with import results
    """
    try:
        # Parse the CSV content
        csv_reader = csv.DictReader(io.StringIO(content_str))
        
        imported_count = 0
        errors = []
        parsed_items = []
        
        # Required fields for an item
        required_fields = [
            "itemId", "name", "width", "depth", "height", 
            "priority", "expiryDate", "usageLimit", "preferredZone"
        ]
        
        # Process each row in the CSV
        for row_num, row in enumerate(csv_reader, start=1):
            try:
                # Check if all required fields are present
                missing_fields = [field for field in required_fields if field not in row or not row[field]]
                if missing_fields:
                    errors.append(ImportError(
                        row=row_num,
                        message=f"Missing required fields: {', '.join(missing_fields)}"
                    ))
                    continue
                
                # Convert numeric fields
                try:
                    row['width'] = int(row['width'])
                    row['depth'] = int(row['depth'])
                    row['height'] = int(row['height'])
                    row['priority'] = int(row['priority'])
                except ValueError:
                    errors.append(ImportError(
                        row=row_num,
                        message="Width, depth, height, and priority must be valid numbers"
                    ))
                    continue
                
                # Add the validated row to our parsed items
                parsed_items.append(row)
                imported_count += 1
                
            except Exception as e:
                errors.append(ImportError(
                    row=row_num,
                    message=f"Error processing row: {str(e)}"
                ))
        
        return ImportResponse(
            success=True,
            itemsImported=imported_count,
            errors=errors
        ), parsed_items
        
    except Exception as e:
        return ImportResponse(
            success=False,
            itemsImported=0,
            errors=[ImportError(row=0, message=f"Error processing file: {str(e)}")]
        ), []

def import_containers_algorithm(content_str: str) -> Tuple[ImportResponse, List[Dict[str, Any]]]:
    """
    Algorithm to import containers from a CSV file
    
    Args:
        content_str: CSV content as a string
        
    Returns:
        Tuple of (ImportResponse with import results, List of parsed containers)
    """
    try:
        # Parse the CSV content
        csv_reader = csv.DictReader(io.StringIO(content_str))
        
        imported_count = 0
        errors = []
        parsed_containers = []
        
        # Required fields for a container
        required_fields = [
            "containerId", "zone", "width", "depth", "height"
        ]
        
        # Process each row in the CSV
        for row_num, row in enumerate(csv_reader, start=1):
            try:
                # Check if all required fields are present
                missing_fields = [field for field in required_fields if field not in row or not row[field]]
                if missing_fields:
                    errors.append(ImportError(
                        row=row_num,
                        message=f"Missing required fields: {', '.join(missing_fields)}"
                    ))
                    continue
                
                # Convert numeric fields
                try:
                    row['width'] = int(row['width'])
                    row['depth'] = int(row['depth'])
                    row['height'] = int(row['height'])
                except ValueError:
                    errors.append(ImportError(
                        row=row_num,
                        message="Width, depth, and height must be valid numbers"
                    ))
                    continue
                
                # Add the validated row to our parsed containers
                parsed_containers.append(row)
                imported_count += 1
                
            except Exception as e:
                errors.append(ImportError(
                    row=row_num,
                    message=f"Error processing row: {str(e)}"
                ))
        
        return ImportResponse(
            success=True,
            itemsImported=imported_count,
            errors=errors
        ), parsed_containers
        
    except Exception as e:
        return ImportResponse(
            success=False,
            itemsImported=0,
            errors=[ImportError(row=0, message=f"Error processing file: {str(e)}")]
        ), []