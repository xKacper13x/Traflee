from database.models import Incident
from database.schemas import IncidentSchema


def add(session, incident_info: IncidentSchema) -> Incident:
    type = incident_info.incident_type
    description = incident_info.description
    time = incident_info.time
    car_id = incident_info.car_id
    lat = incident_info.lat
    long = incident_info.long

    new_incident = Incident(type=type, description=description, time=time,
                            car_id=car_id, latitude=lat, longitude=long)
    session.add(new_incident)
    session.commit()
    return new_incident


def get_by_id(session, incident_id: int) -> Incident | None:
    return session.query(Incident).filter(incident_id == incident_id).first()
