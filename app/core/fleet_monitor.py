from app.database.models import Car
from app.database.crud import dtc_code
from app.services.deposit_validator import DepositValidator
from app.services.dtc_translator import DTCTranslator
from app.database.schemas import DTCCodeSchema
from dataclasses import dataclass
import time


@dataclass
class CycleResult:
    codes_translation: list
    codes_to_save: list
    incidents: dict


class FleetMonitor:
    def __init__(self, session):
        self._deposit_validator = DepositValidator()
        self._translator = DTCTranslator()
        self._session = session
        self._prev_states = {}

    def run_cycle(self, car_info: Car,
                  current_metrics: dict, dtc_codes: list
                  ) -> CycleResult:
        car_id = car_info.id
        fuel_type = car_info.fuel_type
        car_profile = car_info.car_profile
        car_brand = car_info.car_brand

        codes_translation = []
        codes_to_save = []
        for error in dtc_codes:
            code = error['code']
            raw_description = error['description']
            code_in_base = dtc_code.find_dtc_translation(self._session, code,
                                                         car_profile,
                                                         car_brand, fuel_type)
            if code_in_base is not None:
                codes_translation.append({
                        'code': code,
                        'raw_description': raw_description,
                        'severity': code_in_base.severity,
                        'manager_explanation':
                        code_in_base.manager_explanation,
                        'action_required': code_in_base.action_required,
                        'is_verified': code_in_base.is_verified
                    }
                )
            else:
                response = self._translator.analyze_error(code,
                                                          raw_description,
                                                          fuel_type,
                                                          car_profile,
                                                          car_brand)
                codes_translation.append({
                        'code': code,
                        'raw_description': raw_description,
                        'severity': response.severity,
                        'manager_explanation':
                        response.manager_explanation,
                        'action_required': response.action_required,
                        'is_verified': False
                    }
                )

                new_code = DTCCodeSchema(code=code, car_type=car_profile, car_brand=car_brand,
                                         fuel_type=fuel_type, severity=response.severity,
                                         manager_explanation=response.manager_explanation,
                                         action_required=response.action_required,
                                         is_verified=False)
                codes_to_save.append(new_code)

        prev_state = self._prev_states.get(car_id, {'rpm': current_metrics['rpm'],
                                                    'timestamp': time.time()})
        new_incidents, curr_state = self._deposit_validator.validate_frame(
                                                    current_metrics, car_id,
                                                    fuel_type, prev_state)
        self._prev_states[car_id] = curr_state
        return CycleResult(codes_translation, codes_to_save,
                           new_incidents)
