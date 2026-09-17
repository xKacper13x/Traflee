from app.database.models import Car
from app.database.schemas import CarSchema


def add(session, car_data: CarSchema) -> Car:
    new_car = Car(**car_data.model_dump())

    session.add(new_car)
    session.commit()
    session.refresh(new_car)

    return new_car


def get_by_devide_id(session, device_id: str) -> Car | None:
    return session.query(Car).filter(Car.device_id == device_id).first()


def get_by_id(session, car_id: int) -> Car | None:
    return session.query(Car).filter(Car.id == car_id).first()
