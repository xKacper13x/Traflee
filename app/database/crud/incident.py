from app.database.models import Incident
from app.schemas.incident_schemas import IncidentCreate
from app.database.models import Car


def add(session, incident_info: IncidentCreate) -> Incident:
    new_incident = Incident(**incident_info.model_dump())

    session.add(new_incident)
    session.commit()
    session.refresh(new_incident)

    return new_incident


def get_by_id(session, incident_id: int) -> Incident | None:
    return session.query(Incident).filter(
        Incident.id == incident_id
        ).first()


def get_incidents_by_rental(session, rental_id: int) -> list[Incident]:
    return session.query(Incident).join(Incident.car).filter(Car.rental_id == rental_id).order_by(Incident.time.desc()).all()


def get_by_car_id(session, car_id: int) -> list[Incident]:
    return session.query(Incident).filter(Incident.car_id == car_id).order_by(Incident.time.desc()).all()
