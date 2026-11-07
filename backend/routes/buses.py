
from fastapi import APIRouter, HTTPException
from database import buses_collection
from models import Bus

router = APIRouter(prefix="/api/buses", tags=["Buses"])


@router.get("/")
def get_all_buses():

    buses = list(buses_collection.find({}, {"_id": 0}))

    return buses


@router.get("/{bus_id}")
def get_bus(bus_id: str):

    bus = buses_collection.find_one(
        {"bus_id": bus_id},
        {"_id": 0}
    )

    if bus is None:
        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )

    return bus


@router.post("/")
def create_bus(bus: Bus):

    if buses_collection.find_one({"bus_id": bus.bus_id}):
        raise HTTPException(
            status_code=409,
            detail="Bus already exists"
        )

    bus_data = bus.model_dump()

    bus_data["status"] = "Quiet"
    bus_data["occupancy_percentage"] = 0
    bus_data["available_seats"] = bus.capacity - bus.current_passengers

    buses_collection.insert_one(bus_data)

    return {
        "message": "Bus created successfully",
        "bus": bus_data
    }
