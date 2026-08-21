from database.models import User
from database.schemas import UserSchema


def add(session, user_data: UserSchema) -> User:
    pass_hash = get_password_hash(user_data.password)

    new_user = User(email=user_data.email,
                    password_hash=pass_hash,
                    rental_id=user_data.rental_id)
    session.add(new_user)
    session.commit()
    return new_user


def get_by_id(session, user_id: int) -> User | None:
    return session.query(User).filter(User.id == user_id).first()


def get_by_email(session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()


def get_password_hash(password: str) -> str:
    # tu napisać hashowanie
    return password
