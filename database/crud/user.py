from database.models import User


def add(session, email: str, password: str, rental_id: int) -> User:
    new_user = User(email=email, password=password,
                    rental_id=rental_id)
    session.add(new_user)
    session.commit()
    return new_user


def get_by_id(session, user_id: int) -> User | None:
    return session.query(User).filter(User.id == user_id).first()


def get_by_email(session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()
