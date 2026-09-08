from passlib.context import CryptContext
from app.database.models import User
from app.database.schemas import UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def add(session, user_data: UserSchema) -> User:
    data_dict = user_data.model_dump()

    raw_password = data_dict.pop('password')
    data_dict['password_hash'] = get_password_hash(raw_password)

    new_user = User(**data_dict)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


def get_by_id(session, user_id: int) -> User | None:
    return session.query(User).filter(User.id == user_id).first()


def get_by_email(session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
