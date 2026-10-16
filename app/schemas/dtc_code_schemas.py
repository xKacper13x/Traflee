from app.core.enums import FuelType, DTCCodeSeverity
from pydantic import BaseModel


class DTCCodeBase(BaseModel):
    code: str
    car_type: str
    car_brand: str
    fuel_type: FuelType
    severity: DTCCodeSeverity
    manager_explanation: str
    action_required: str
    is_verified: bool
