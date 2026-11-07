
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone

from database import buses_collection, sensor_readings_collection
from models import SensorReading

router = APIRouter(
    prefix="/api/sensors",
    tags=["Sensors"]
)


@router.post("/readings")
def receive_sensor_reading(reading: SensorReading):

    bus = buses_collection.find_one(
        {"bus_id": reading.bus_id}
    )

    if bus is None:
        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )

    timestamp = datetime.now(timezone.utc)

    sensor_data = reading.model_dump()
    sensor_data["timestamp"] = timestamp

    sensor_readings_collection.insert_one(sensor_data)

    buses_collection.update_one(
        {"bus_id": reading.bus_id},
        {
            "$set": {
                "sensor_id": reading.sensor_id,
                "motion_detected": reading.motion_detected,
                "sensor_status": "Healthy",
                "sensor_last_updated": timestamp
            }
        }
    )

    return {
        "message": "Sensor reading received successfully",
        "sensor_id": reading.sensor_id,
        "motion_detected": reading.motion_detected,
        "sensor_status": "Healthy"
    }


@router.get("/{bus_id}/status")
def get_sensor_status(bus_id: str):

    bus = buses_collection.find_one(
        {"bus_id": bus_id},
        {"_id": 0}
    )

    if bus is None:
        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )

    return {
        "bus_id": bus_id,
        "sensor_id": bus.get("sensor_id", "MOTION_01"),
        "sensor_status": bus.get("sensor_status", "Not connected"),
        "motion_detected": bus.get("motion_detected", False),
        "last_updated": bus.get("sensor_last_updated")
    }
