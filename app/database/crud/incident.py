from app.database.models import Incident
from app.database.schemas import IncidentSchema


def add(session, incident_info: IncidentSchema) -> Incident:
    new_incident = Incident(**incident_info.model_dump())

    session.add(new_incident)
    session.commit()
    session.refresh(new_incident)

    return new_incident


def get_by_id(session, incident_id: int) -> Incident | None:
    return session.query(Incident).filter(
        Incident.id == incident_id
        ).first()
