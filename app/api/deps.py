from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db_config import SessionLocal
from app.database.crud import car as car_crud
from app.database.crud import user as user_crud
from app.database.models import Car, User


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_current_user(db: Session = Depends(get_db)) -> User:
    user = user_crud.get_by_id(db, 1)

    if not user:
        raise HTTPException(status_code=401, detail='User not authorized')

    return user


def get_rental_id(user: User = Depends(get_current_user)) -> int:
    return user.rental_id


def get_car(car_id: int,
            rental_id: int = Depends(get_rental_id),
            db: Session = Depends(get_db)) -> Car:
    car = car_crud.get_by_id_for_rental(db, car_id, rental_id)
    if not car:
        raise HTTPException(status_code=404, detail='Car not found')

    return car
