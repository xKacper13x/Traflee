from fastapi import FastAPI, Depends, HTTPException
from app.schemas.incident_schemas import IncidentResponse
from app.api.deps import get_db, get_rental_id, get_car
from sqlalchemy.orm import Session
from app.database.crud import incident as incident_crud
from app.database.models import Car
from typing import List


api = FastAPI()


@api.get('/incidents', response_model=List[IncidentResponse])
def get_incidents(db: Session = Depends(get_db),
                  rental_id: int = Depends(get_rental_id)):
    return incident_crud.get_incidents_by_rental(db, rental_id)


@api.get('/incidents/{incident_id}', response_model=IncidentResponse)
def get_incident_by_id(incident_id: int,
                       db: Session = Depends(get_db),
                       rental_id: int = Depends(get_rental_id)):
    incident = incident_crud.get_by_id(db, incident_id)

    if not incident or incident.car.rental_id != rental_id:
        raise HTTPException(status_code=404, detail='Incident not found')

    return incident


@api.get('/cars/{car_id}/incidents', response_model=List[IncidentResponse])
def get_incidents_by_car_id(car: Car = Depends(get_car),
                            db: Session = Depends(get_db)):
    return incident_crud.get_by_car_id(db, car.id)
