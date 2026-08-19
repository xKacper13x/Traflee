from models import Car


def add(session, rental_id: int, vin: str = None) -> Car:
    new_car = Car(rental_id=rental_id, vin=vin)
    session.add(new_car)
    session.commit()
    return new_car


def get_by_id(session, car_id: int) -> Car | None:
    return session.query(Car).filter(Car.id == car_id).first()
