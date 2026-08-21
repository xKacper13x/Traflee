from dataclasses import dataclass
from datetime import datetime


@dataclass
class IncidentSchema:
    incident_type: int
    description: str
    time: datetime
    car_id: int
    lat: float
    long: float


@dataclass
class CarSchema:
    rental_id: int
    vin: str


@dataclass
class UserSchema:
    email: str
    password: str
    rental_id: int
