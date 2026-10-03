from pydantic import BaseModel
from datetime import datetime
from app.core.enums import FuelType, IncidentType, DTCCodeSeverity


class IncidentSchema(BaseModel):
    type: IncidentType
    description: str
    time: datetime
    car_id: int
    latitude: float
    longitude: float


class CarSchema(BaseModel):
    vin: str
    device_id: str
    rental_id: int
    fuel_type: FuelType
    car_profile: str
    car_brand: str


class UserSchema(BaseModel):
    email: str
    password: str
    rental_id: int


class DTCCodeSchema(BaseModel):
    code: str
    car_type: str
    car_brand: str
    fuel_type: FuelType
    severity: DTCCodeSeverity
    manager_explanation: str
    action_required: str
    is_verified: bool
