from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["stellar_stash"]

items_collection = db["items"]
containers_collection = db["containers"]
