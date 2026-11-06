
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select database
database = client["bus_tracker"]

# Select collections
buses_collection = database["buses"]
occupancy_collection = database["occupancy"]

# Test connection 
try:
    client.admin.command("ping")
    print("Connected to MongoDB successfully!")
except Exception as e:
    print("MongoDB connection failed:", e)
