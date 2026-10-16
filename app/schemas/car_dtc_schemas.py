from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class CarDTCBase(BaseModel):
    car_id: int
    dtc_id: int
    detected_at: datetime
    resolved_at: datetime
    is_active: bool


class CarDTCResponse(CarDTCBase):
    id: int = Field(..., description='Unique identifier of the vehicle.')

    model_config = ConfigDict(from_attributes=True)


class CarDTCCreate(CarDTCBase):
    pass
