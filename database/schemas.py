from dataclasses import dataclass
from datetime import datetime
from enums import FuelType, IncidentType


@dataclass
class IncidentSchema:
    incident_type: IncidentType
    description: str
    time: datetime
    car_id: int
    lat: float
    long: float


@dataclass
class CarSchema:
    vin: str
    rental_id: int
    fuel_type: FuelType


@dataclass
class UserSchema:
    email: str
    password: str
    rental_id: int
