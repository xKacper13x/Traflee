from pwdlib import PasswordHash
from app.database.models import User
from app.schemas.schemas import UserSchema

password_hash = PasswordHash.recommended()


def add(session, user_data: UserSchema) -> User:
    data_dict = user_data.model_dump()

    raw_password = data_dict.pop('password')
    data_dict['password_hash'] = hash_password(raw_password)

    new_user = User(**data_dict)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


def get_by_id(session, user_id: int) -> User | None:
    return session.query(User).filter(User.id == user_id).first()


def get_by_email(session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)
