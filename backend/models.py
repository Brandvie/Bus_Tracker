
from pydantic import BaseModel, Field
from typing import Literal
from typing import Optional

class MovementRequest(BaseModel):
    direction: Literal ["in", "out"]
    quantity: int = Field(default=1, ge=1, le=25)


class PassengerCountRequest(BaseModel):
    current_passengers: int = Field(
        ge=0,
        le=25
    )


class BusResponse(BaseModel):
    bus_id: str
    capacity: int
    current_passengers: int
    crowd_status: str
    motion_detected: bool
    active: bool





class SensorReading(BaseModel):
    bus_id: str
    sensor_id: str
    motion_detected: bool
    sensor_type: str = "PIR"
    timestamp: Optional[str] = None
