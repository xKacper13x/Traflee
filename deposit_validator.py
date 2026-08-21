from exceptions import MissingParams
from database.schemas import IncidentSchema
from datetime import datetime
from enums import IncidentType, FuelType


class DepositValidator:
    def __init__(self):
        self._incidents = {
            IncidentType.COLD_ENGINE: [],
            IncidentType.REDLINING: []
        }

    def _check_thrashing_cold_engine(self, coolant_temp, oil_temp,
                                     rpm, engine_load) -> bool:
        if rpm is None or engine_load is None or coolant_temp is None:
            raise MissingParams

        is_cold = False
        if oil_temp is not None:
            if oil_temp < 70:
                is_cold = True
        elif coolant_temp < 80:
            is_cold = True

        if is_cold:
            if engine_load > 60:
                return True

            if rpm > 3500 and engine_load > 20:
                return True

        return False

    def _check_redlining(self, rpm, fuel_type: FuelType) -> bool:
        pass

    def _create_schema(self, coolant_temp, oil_temp,
                       rpm, engine_load, desc: str) -> IncidentSchema:
        new_incident = IncidentSchema(IncidentType.COLD_ENGINE,
                                      desc, datetime.now(), 1, 0, 0)
        return new_incident

    def check_deposit_rules(self, data: dict) -> dict:
        coolant_temp = data.get('coolant_temp')
        oil_temp = data.get('oil_temp')
        rpm = data.get('rpm')
        load = data.get('load')

        res = {
            'status': True,
            'schemas': None,
            'comment': 'Jazda prawidłowa'
        }

        comment = 'Jazda prawidłowa'

        new_incidents = []
        try:
            if self._check_thrashing_cold_engine(coolant_temp, oil_temp,
                                                 rpm, load):
                new_incidents.append(IncidentType.COLD_ENGINE)
            if self._check_redlining():
                new_incidents.append(IncidentType.REDLINING)
        except MissingParams:
            comment = "BŁĄD: Brak wystarczających danych z czujników do oceny"

        if new_incidents:
            new_schema = self._create_schema(coolant_temp, oil_temp,
                                             rpm, load, comment)
            self._incident_list.append(new_schema)
            if len(self._incident_list) > 3:
                res['status'] = False
                res['schemas'] = self._incident_list
                res['comment'] = comment
        else:
            self._incident_list.clear()

        return res
