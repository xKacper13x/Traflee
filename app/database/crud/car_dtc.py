from app.database.models import CarDTC, Car
from app.schemas.car_dtc_schemas import CarDTCCreate


def add(session, code_data: CarDTCCreate) -> CarDTC:
    new_code = CarDTC(**code_data.model_dump())

    session.add(new_code)
    session.commit()
    session.refresh(new_code)

    return new_code


def get_dtc_codes_by_rental(session, rental_id: int) -> list[CarDTC]:
    return session.query(CarDTC).join(CarDTC.car).filter(Car.rental_id == rental_id).order_by(CarDTC.detected_at).all()


def get_dtc_codes_by_car(session, car_id: int) -> list[CarDTC]:
    return session.query(CarDTC).filter(CarDTC.car_id == car_id).all()


def get_by_id(session, code_id: int) -> CarDTC | None:
    return session.query(CarDTC).filter(CarDTC.id == code_id).first()
