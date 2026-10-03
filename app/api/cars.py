from fastapi import FastAPI, Depends
from app.database.models import Car
from app.api.deps import get_rental_id, get_db, get_car
from app.database.crud import car as car_crud
from app.schemas.car_schemas import CarCreate, CarResponse, CarUpdate
from sqlalchemy.orm import Session
from typing import List


api = FastAPI()


@api.get('/cars', response_model=List[CarResponse])
def get_cars(db: Session = Depends(get_db),
             rental_id: int = Depends(get_rental_id)):
    return car_crud.get_cars_by_rental(db, rental_id)


@api.get('/cars/{car_id}', response_model=CarResponse)
def get_car_by_id(car: Car = Depends(get_car)):
    return car


@api.post('/cars', status_code=201, response_model=CarResponse)
def add_car(new_car: CarCreate,
            db: Session = Depends(get_db),
            rental_id: int = Depends(get_rental_id)):
    return car_crud.add(db, new_car, rental_id)


@api.patch('/cars/{car_id}', response_model=CarResponse)
def update_car(updated_car: CarUpdate,
               car: int = Depends(get_car),
               db: Session = Depends(get_db)):
    return car_crud.update_car(db, car, updated_car)


@api.delete('/cars/{car_id}', status_code=204)
def delete_car(car: Car = Depends(get_car),
               db: Session = Depends(get_db)):
    car_crud.delete_car(db, car)
