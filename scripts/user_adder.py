from app.services.car_data_reader import CarDataReader
from app.database.db_config import engine, SessionLocal
from app.database.crud import incident as incident_crud
from app.schemas.incident_schemas import IncidentCreate
import app.database.models as models
from app.core.enums import IncidentType
from datetime import datetime


models.Base.metadata.create_all(engine)
session = SessionLocal()

# user_data = UserSchema(email='kacperkrzyzewski20@gmail.com',
#                        password='Tak',
#                        rental_id=1)
incident_data = IncidentCreate(type=IncidentType.COLD_ENGINE,
                               description='thrashing', time=datetime.now(),
                               car_id=3, latitude=0, longitude=0)

incident_crud.add(session, incident_data)

session.close()
