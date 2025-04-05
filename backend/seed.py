from db import items_collection, containers_collection

items = [
    {
        "id": "001",
        "name": "Food Packet",
        "width": 10,
        "depth": 10,
        "height": 20,
        "mass": 5,
        "priority": 80,
        "expiryDate": "2025-05-20",
        "usageLimit": "30 uses",
        "preferredZone": "Crew Quarters",
    },
    {
        "id": "002",
        "name": "Oxygen Cylinder",
        "width": 15,
        "depth": 15,
        "height": 50,
        "mass": 30,
        "priority": 95,
        "expiryDate": "N/A",
        "usageLimit": "100 uses",
        "preferredZone": "Airlock",
    },
]

containers = [
    {
        "zone": "Crew Quarters",
        "containerId": "contA",
        "width": 100,
        "depth": 85,
        "height": 200,
    },
    {
        "zone": "Airlock",
        "containerId": "contB",
        "width": 50,
        "depth": 85,
        "height": 200,
    },
]

# Wipe and insert
items_collection.delete_many({})
items_collection.insert_many(items)

containers_collection.delete_many({})
containers_collection.insert_many(containers)

print("✅ Sample data seeded.")
