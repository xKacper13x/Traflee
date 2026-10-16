from pydantic import BaseModel
from datetime import datetime
from app.core.enums import FuelType, IncidentType, DTCCodeSeverity


class UserSchema(BaseModel):
    email: str
    password: str
    rental_id: int
