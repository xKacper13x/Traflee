from app.core.exceptions import MissingParams
from app.database.schemas import IncidentSchema
from datetime import datetime
from app.core.enums import IncidentType, FuelType


class DepositValidator:
    def __init__(self):
        self._incidents = {
            IncidentType.COLD_ENGINE: [],
            IncidentType.REDLINING: [],
            IncidentType.PEELING_OUT: []
        }

        self._MAX_SPEED = 20
        self._MIN_RPM_SPIKE_PER_SEC = {
            FuelType.PETROL: 1500,
            FuelType.DIESEL: 1000
        }
        self._MIN_RPM_BURNOUT = {
            FuelType.PETROL: 4500,
            FuelType.DIESEL: 2800
        }
        self._MAX_COLD_RPM = {
            FuelType.PETROL: 3800,
            FuelType.DIESEL: 3200
        }
        self._REDLINE_RPM_DRIVING = {
            FuelType.PETROL: 6500,
            FuelType.DIESEL: 4500
        }

    def _check_thrashing_cold_engine(self, coolant_temp, oil_temp,
                                     rpm, engine_load, fuel_type) -> bool:
        if rpm is None or engine_load is None or coolant_temp is None:
            raise MissingParams

        if oil_temp is not None:
            is_cold = oil_temp < 65
        else:
            is_cold = coolant_temp < 70

        if not is_cold:
            return False

        if rpm > self._MAX_COLD_RPM.get(fuel_type, 3800):
            return True

        if engine_load > 92:
            if fuel_type == FuelType.PETROL and rpm > 2500:
                return True
            if fuel_type == FuelType.DIESEL and rpm > 2000:
                return True

        return False

    def _check_redlining(self, rpm, speed, fuel_type) -> bool:
        if rpm is None or speed is None:
            return False

        if rpm > self._REDLINE_RPM_DRIVING.get(fuel_type, 6500):
            return True

        if speed < 5:
            if fuel_type == FuelType.PETROL and rpm > 3800:
                return True
            if fuel_type == FuelType.DIESEL and rpm > 3000:
                return True

        return False

    def _check_peeling_out(self, current_data: dict, previous_state: dict,
                           fuel_type: FuelType) -> tuple[bool, dict]:
        rpm = current_data.get('rpm')
        speed = current_data.get('speed')
        current_time = current_data.get('timestamp')

        new_state = {
            'rpm': rpm,
            'timestamp': current_time
        }

        if None in (speed, rpm, current_time):
            return False, new_state

        prev_rpm = previous_state.get('rpm', rpm)
        prev_time = previous_state.get('timestamp', current_time)

        time_delta = current_time - prev_time

        if time_delta <= 0:
            time_delta = 0.001
        elif time_delta > 3.0:
            return False, new_state

        rpm_spike_per_sec = (rpm - prev_rpm) / time_delta
        is_peeling_out = False

        if speed < self._MAX_SPEED:
            if rpm_spike_per_sec > self._MIN_RPM_SPIKE_PER_SEC[fuel_type] or rpm > self._MIN_RPM_BURNOUT[fuel_type]:
                is_peeling_out = True

        return is_peeling_out, new_state

    def _create_schema(self, incident_type, coolant_temp, oil_temp,
                       rpm, engine_load, desc: str,
                       car_id: int) -> IncidentSchema:
        new_incident = IncidentSchema(incident_type, desc,
                                      datetime.now(), car_id, 0, 0)
        return new_incident

    def validate_frame(self, data: dict, car_id: int,
                       fuel_type: FuelType,
                       previous_state: dict) -> tuple[dict, dict]:
        coolant_temp = data.get('coolant_temp')
        oil_temp = data.get('oil_temp')
        rpm = data.get('rpm')
        speed = data.get('speed')
        load = data.get('load')

        new_incidents = []
        try:
            if self._check_thrashing_cold_engine(coolant_temp, oil_temp,
                                                 rpm, load, fuel_type):
                desc = 'Katuje auto na zimnym'
                new_incidents.append((IncidentType.COLD_ENGINE, desc))
            else:
                self._incidents[IncidentType.COLD_ENGINE].clear()
        except MissingParams:
            comment = "BŁĄD: Brak wystarczających danych z czujników do oceny"

        is_peeling_out, new_state = self._check_peeling_out(data,
                                                            previous_state,
                                                            fuel_type)
        if is_peeling_out:
            desc = 'Start z piskiem'
            new_incidents.append((IncidentType.PEELING_OUT, desc))
        else:
            self._incidents[IncidentType.PEELING_OUT].clear()

        if self._check_redlining(rpm, speed, fuel_type):
            desc = 'Odcinka'
            new_incidents.append((IncidentType.REDLINING, desc))
        else:
            self._incidents[IncidentType.REDLINING].clear()

        res = {}
        for incident, desc in new_incidents:
            new_incident_schema = self._create_schema(incident, coolant_temp,
                                                      oil_temp, rpm, load,
                                                      desc, car_id)
            self._incidents[incident].append(new_incident_schema)

            if incident == IncidentType.PEELING_OUT or len(self._incidents[incident]) > 3:
                res[incident] = list(self._incidents[incident])
                self._incidents[incident].clear()

        return res, new_state
