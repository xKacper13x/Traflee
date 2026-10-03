from app.services.car_data_reader import CarDataReader
from app.database.db_config import engine, SessionLocal
from app.database.crud import user as user_crud
from app.schemas.schemas import UserSchema
import app.database.models as models


models.Base.metadata.create_all(engine)
session = SessionLocal()

user_data = UserSchema(email='kacperkrzyzewski20@gmail.com',
                       password='Tak',
                       rental_id=1)
user_crud.add(session, user_data)

session.close()
