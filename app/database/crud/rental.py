from app.database.models import Rental


def add(session, name: str) -> Rental:
    new_rental = Rental(name=name)

    session.add(new_rental)
    session.commit()

    return new_rental


def get_by_id(session, rental_id: int) -> Rental | None:
    return session.query(Rental).filter(rental_id == rental_id).first()
