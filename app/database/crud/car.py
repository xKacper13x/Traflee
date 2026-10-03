from app.database.models import Car
from app.schemas.car_schemas import CarCreate, CarUpdate


def add(session, car_data: CarCreate, rental_id: int) -> Car:
    new_car = Car(**car_data.model_dump(), rental_id=rental_id)

    session.add(new_car)
    session.commit()
    session.refresh(new_car)

    return new_car


def get_by_device_id(session, device_id: str) -> Car | None:
    return session.query(Car).filter(Car.device_id == device_id).first()


def get_by_id(session, car_id: int) -> Car | None:
    return session.query(Car).filter(Car.id == car_id).first()


def get_by_id_for_rental(session, car_id: int, rental_id: int) -> Car | None:
    return session.query(Car).filter(Car.id == car_id, Car.rental_id == rental_id).first()


def get_cars_by_rental(session, rental_id: int) -> list[Car]:
    return session.query(Car).filter(Car.rental_id == rental_id).all()


def update_car(session, car: Car, updated_car_data: CarUpdate) -> Car:
    update_data = updated_car_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(car, field, value)

    session.commit()
    session.refresh

    return car


def delete_car(session, car: Car) -> None:
    session.delete(car)
    session.commit()
