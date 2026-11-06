
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


def check_database_connection():
    try:
        client.admin.command("ping")
        return True
    except Exception:
        return False
