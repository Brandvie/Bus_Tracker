
from pydantic import BaseModel, Field
from typing import Optional


class Bus(BaseModel):
    bus_id: str
    route: str
    capacity: int = Field(gt=0)
    current_passengers: int = Field(ge=0)
    active: bool = True


class OccupancyUpdate(BaseModel):
    bus_id: str
    passenger_count: int = Field(ge=0)


class SensorReading(BaseModel):
    bus_id: str
    sensor_id: str
    motion_detected: bool
    sensor_type: str = "PIR"
    timestamp: Optional[str] = None
