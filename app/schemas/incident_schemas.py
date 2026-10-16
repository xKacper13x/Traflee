from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from app.core.enums import IncidentType


class IncidentBase(BaseModel):
    type: IncidentType = Field(..., description='')
    description: str = Field(..., description='')
    time: datetime = Field(..., description='')
    car_id: int = Field(..., description='')
    latitude: float = Field(..., description='')
    longitude: float = Field(..., description='')


class IncidentResponse(IncidentBase):
    id: int = Field(..., description='')

    model_config = ConfigDict(from_attributes=True)


class IncidentCreate(IncidentBase):
    pass
