
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone

from database import buses_collection, occupancy_collection
from models import OccupancyUpdate
from occupancy import calculate_occupancy

router = APIRouter(
    prefix="/api/buses",
    tags=["Occupancy"]
)


@router.get("/{bus_id}/occupancy")
def get_bus_occupancy(bus_id: str):

    bus = buses_collection.find_one(
        {"bus_id": bus_id},
        {"_id": 0}
    )

    if bus is None:
        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )

    return calculate_occupancy(
        bus["current_passengers"],
        bus["capacity"]
    )


@router.post("/simulation/occupancy")
def update_occupancy(update: OccupancyUpdate):

    bus = buses_collection.find_one(
        {"bus_id": update.bus_id}
    )

    if bus is None:
        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )

    if update.passenger_count > bus["capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Passenger count exceeds capacity"
        )

    result = calculate_occupancy(
        update.passenger_count,
        bus["capacity"]
    )

    timestamp = datetime.now(timezone.utc)

    buses_collection.update_one(
        {"bus_id": update.bus_id},
        {
            "$set": {
                "current_passengers": update.passenger_count,
                "occupancy_percentage": result["occupancy_percentage"],
                "available_seats": result["available_seats"],
                "status": result["status"],
                "last_updated": timestamp
            }
        }
    )

    occupancy_collection.insert_one({
        "bus_id": update.bus_id,
        **result,
        "timestamp": timestamp
    })

    return {
        "message": "Occupancy updated successfully",
        **result
    }


@router.get("/{bus_id}/history")
def get_occupancy_history(bus_id: str):

    bus = buses_collection.find_one(
        {"bus_id": bus_id}
    )

    if bus is None:
        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )

    history = list(
        occupancy_collection.find(
            {"bus_id": bus_id},
            {"_id": 0}
        ).sort("timestamp", -1).limit(50)
    )

    return history
