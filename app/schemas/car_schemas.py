
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.core.enums import FuelType


class CarBase(BaseModel):
    vin: str = Field(..., description='VIN of the vehicle.')
    device_id: str = Field(..., description='Unique identifier of the device.')
    fuel_type: FuelType = Field(..., description='')
    car_profile: str = Field(..., description='')
    car_brand: str = Field(..., description='')


class CarCreate(CarBase):
    pass


class CarResponse(CarBase):
    id: int = Field(..., description='Unique identifier of the vehicle.')
    rental_id: int = Field(..., description='Unique identifier of the rental.')

    model_config = ConfigDict(from_attributes=True)


class CarUpdate(CarBase):
    vin: Optional[str] = Field(None, description='VIN of the vehicle.')
    device_id: Optional[str] = Field(None, description='')
    fuel_type: Optional[FuelType] = Field(None, description='')
    car_profile: Optional[str] = Field(None, description='')
    car_brand: Optional[str] = Field(None, description='')
