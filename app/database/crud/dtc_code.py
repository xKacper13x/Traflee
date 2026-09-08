from app.database.models import DTCCode
from app.database.schemas import DTCCodeSchema
from app.core.enums import FuelType


def add(session, code_data: DTCCodeSchema) -> DTCCode:
    new_code = DTCCode(**code_data.model_dump())

    session.add(new_code)
    session.commit()
    session.refresh(new_code)

    return new_code


def get_by_id(session, code_id: int) -> DTCCode | None:
    return session.query(DTCCode).filter(DTCCode.id == code_id).first()


def find_dtc_translation(session, code: str, car_type: str, car_brand: str,
                         fuel_type: FuelType) -> DTCCode | None:
    return session.query(DTCCode).filter(
        DTCCode.code == code,
        DTCCode.car_type == car_type,
        DTCCode.car_brand == car_brand,
        DTCCode.fuel_type == fuel_type
    ).first()
