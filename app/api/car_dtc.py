from fastapi import FastAPI, Depends
from app.api.deps import get_db, get_rental_id
from app.schemas.car_dtc_schemas import CarDTCResponse
from sqlalchemy.orm import Session
from app.database.crud import car_dtc as car_dtc_crud


api = FastAPI()


@api.get('/car_dtc/{dtc_id}', response_model=CarDTCResponse)
def get_car_dtc_by_id(dtc_id: int,
                      db: Session = Depends(get_db)):
    return car_dtc_crud.get_by_id(db, dtc_id)


@api.get('/car_dtc', response_model=list[CarDTCResponse])
def get_dtc_codes(db: Session = Depends(get_db),
                  rental_id: int = Depends(get_rental_id)):
    return car_dtc_crud.get_dtc_codes_by_rental(db, rental_id)


@api.get('/cars/{car_id}/car_dtc', response_model=list[CarDTCResponse])
def get_codes_by_car_id(car_id: int,
                        db: Session = Depends(get_db)) -> list[CarDTCResponse]:
    return car_dtc_crud.get_dtc_codes_by_car(db, car_id)
