
from fastapi import APIRouter, HTTPException

from database import buses_collection

router = APIRouter(
    prefix="/api/buses",
    tags=["Buses"]
)


@router.get("/")
def get_all_buses():

    buses = list(
        buses_collection.find(
            {},
            {"_id": 0}
        )
    )

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
