
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone

from database import ( 
    buses_collection, 
    occupancy_collection)
from models import (
    MovementRequest,
    PassengerCountRequest
)
from occupancy import (
    calculate_crowd_status,
    calculate_passenger_count
)

router = APIRouter(
    prefix="/api/occupancy",
    tags=["Occupancy"]
)

def update_bus_occupancy(bus_id, new_count, motion_detected):
    bus = buses_collection.find_one(
        {"bus_id": bus_id}
    )

    if bus is None:
        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )

    capacity = bus["capacity"]

    new_count = max(0, min(new_count, capacity))

    crowd_status = calculate_crowd_status(new_count)

    buses_collection.update_one(
        {"bus_id": bus_id},
        {
            "$set": {
                "current_passengers": new_count,
                "crowd_status": crowd_status,
                "motion_detected": motion_detected,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    # Save occupancy history
    occupancy_collection.insert_one({
        "bus_id": bus_id,
        "current_passengers": new_count,
        "capacity": capacity,
        "crowd_status": crowd_status,
        "motion_detected": motion_detected,
        "timestamp": datetime.now(timezone.utc)
    })

    return {
        "bus_id": bus_id,
        "current_passengers": new_count,
        "capacity": capacity,
        "crowd_status": crowd_status,
        "motion_detected": motion_detected
    }


# GET current occupancy
@router.get("/{bus_id}")
def get_occupancy(bus_id: str):

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


# POST passenger movement
@router.post("/{bus_id}/movement")
def update_movement(
    bus_id: str,
    request: MovementRequest
):

    bus = buses_collection.find_one(
        {"bus_id": bus_id}
    )

    if bus is None:
        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )

    current = bus["current_passengers"]

    new_count = calculate_passenger_count(
        current,
        request.direction,
        request.quantity
    )

    return update_bus_occupancy(
        bus_id,
        new_count,
        True
    )


# POST manual passenger count
@router.post("/{bus_id}/count")
def update_count(
    bus_id: str,
    request: PassengerCountRequest
):

    return update_bus_occupancy(
        bus_id,
        request.current_passengers,
        False
    )


# POST reset passenger count
@router.post("/{bus_id}/reset")
def reset_occupancy(bus_id: str):

    return update_bus_occupancy(
        bus_id,
        0,
        False
    )
