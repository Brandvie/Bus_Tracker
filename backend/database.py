
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "bus_tracker"
)

client = MongoClient(MONGO_URI)

database = client[DATABASE_NAME]

buses_collection = database["buses"]
occupancy_collection = database["occupancy"]
sensor_readings_collection = database["sensor_readings"]


def initialize_database():
    
    buses_collection.update_one(
        {"bus_id": "DKIT_BUS_01"},
        {
            "$setOnInsert": {
                "bus_id": "DKIT_BUS_01",
                "capacity": 25,
                "current_passengers": 0,
                "crowd_status": "Quiet",
                "motion_detected": False,
                "active": True
            }
        },
        upsert=True
    )