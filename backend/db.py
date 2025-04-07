from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["stellar_stash"]

items_collection = db["items"]
containers_collection = db["containers"]
logs_collection = db["logs"]  # Add logs collection
placements_collection = db["placements"]

# Test the connection but don't close it
try:
    client.admin.command('ping')
    print("Connected to MongoDB")
except Exception as e:
    print("Error connecting to MongoDB: ", str(e))

# Example functions that should only run when this file is executed directly
def get_items():
    try:
        items = items_collection.find()
        for item in items:
            print(item)
    except Exception as e:
        print("Error fetching items: ", str(e))

def close_client():
    client.close()
    print("MongoDB connection closed")

# Only run these functions when db.py is executed directly
if __name__ == "__main__":
    get_items()
    close_client()