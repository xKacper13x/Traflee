from database.models import Car
from database.schemas import CarSchema


def add(session, car_data: CarSchema) -> Car:
    new_car = Car(rental_id=car_data.rental_id,
                  vin=car_data.vin)
    session.add(new_car)
    session.commit()
    return new_car


# Trzeba przemyśleć czy usuwac auto z bazy, czy tylko  odpinać je od wypożyczalni
# def remove(session, car_id: int) -> None:
#     obj_to_del = session.query(Car).filter(Car.id == car_id).first()
#     session.delete(obj_to_del)
#     session.commit()


def get_by_id(session, car_id: int) -> Car | None:
    return session.query(Car).filter(Car.id == car_id).first()
