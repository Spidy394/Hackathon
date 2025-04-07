from typing import List, Dict, Optional
from models import Item, Container, PlacementResponse, Placement, Rearrangement, Position, Coordinates, SearchResponse, ItemLocation, RetrievalStep

def calculate_placement(items: List[Item], containers: List[Container]) -> PlacementResponse:
    placements = []
    rearrangements = []
    step_counter = 1
    
    zone_containers = {}
    for container in containers:
        if container.zone not in zone_containers:
            zone_containers[container.zone] = []
        zone_containers[container.zone].append(container)
    
    sorted_items = sorted(items, key=lambda x: x.priority, reverse=True)
    
    for item in sorted_items:
        target_containers = zone_containers.get(item.preferredZone, [])
        
        if not target_containers:
            target_containers = [c for containers_list in zone_containers.values() for c in containers_list]
        
        if not target_containers:
            continue
            
        placed = False
        for container in target_containers:
            if (item.width <= container.width and 
                item.depth <= container.depth and 
                item.height <= container.height):
                
                placement = Placement(
                    itemId=item.itemId,
                    containerId=container.containerId,
                    position=Position(
                        startCoordinates=Coordinates(width=0, depth=0, height=0),
                        endCoordinates=Coordinates(
                            width=item.width,
                            depth=item.depth,
                            height=item.height
                        )
                    )
                )
                placements.append(placement)
                
                rearrangement = Rearrangement(
                    step=step_counter,
                    action="place",
                    itemId=item.itemId,
                    toContainer=container.containerId,
                    toPosition=placement.position
                )
                rearrangements.append(rearrangement)
                step_counter += 1
                
                placed = True
                break
        
        if not placed:
            pass
    
    return PlacementResponse(
        success=len(placements) > 0,
        placements=placements,
        rearrangements=rearrangements
    )

def search_item_algorithm(item_data: Dict, container_data: Optional[Dict] = None) -> SearchResponse:
    if not item_data:
        return SearchResponse(success=True, found=False)
    
    if not container_data:
        return SearchResponse(
            success=False, 
            found=True,
            item=None,
            retrievalSteps=[]
        )
    
    position = Position(
        startCoordinates=Coordinates(width=0, depth=0, height=0),
        endCoordinates=Coordinates(
            width=item_data.get("width", 10),
            depth=item_data.get("depth", 10),
            height=item_data.get("height", 10)
        )
    )
    
    item_location = ItemLocation(
        itemId=item_data["itemId"],
        name=item_data["name"],
        containerId=container_data["containerId"],
        zone=container_data["zone"],
        position=position
    )
    
    retrieval_steps = []
    
    if container_data["zone"] == "Airlock":
        if "blocker_item" in item_data:
            blocker_item = item_data["blocker_item"]
            
            retrieval_steps.append(
                RetrievalStep(
                    step=1,
                    action="remove",
                    itemId=blocker_item["itemId"],
                    itemName=blocker_item["name"]
                )
            )
            
            retrieval_steps.append(
                RetrievalStep(
                    step=2,
                    action="setAside",
                    itemId=blocker_item["itemId"],
                    itemName=blocker_item["name"]
                )
            )
            
            retrieval_steps.append(
                RetrievalStep(
                    step=3,
                    action="retrieve",
                    itemId=item_data["itemId"],
                    itemName=item_data["name"]
                )
            )
            
            retrieval_steps.append(
                RetrievalStep(
                    step=4,
                    action="placeBack",
                    itemId=blocker_item["itemId"],
                    itemName=blocker_item["name"]
                )
            )
        else:
            retrieval_steps.append(
                RetrievalStep(
                    step=1,
                    action="retrieve",
                    itemId=item_data["itemId"],
                    itemName=item_data["name"]
                )
            )
    else:
        retrieval_steps.append(
            RetrievalStep(
                step=1,
                action="retrieve",
                itemId=item_data["itemId"],
                itemName=item_data["name"]
            )
        )
    
    return SearchResponse(
        success=True,
        found=True,
        item=item_location,
        retrievalSteps=retrieval_steps
    )