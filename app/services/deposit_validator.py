from app.database.schemas import IncidentSchema
from datetime import datetime
from app.core.enums import IncidentType, FuelType


class DepositValidator:
    def __init__(self):
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

    def _check_thrashing_cold_engine(self, current_data: dict,
                                     fuel_type: FuelType) -> bool:
        """Required keys: 'rpm', 'coolant_temp', 'oil_temp', 'load'."""
        rpm = current_data.get('rpm')
        coolant_temp = current_data.get('coolant_temp')
        oil_temp = current_data.get('oil_temp')
        engine_load = current_data.get('load')

        if None in (coolant_temp, oil_temp, rpm, engine_load, fuel_type):
            return False

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

    def _check_redlining(self, current_data: dict,
                         fuel_type: FuelType) -> bool:
        """Required keys: 'rpm', 'speed'."""
        rpm = current_data.get('rpm')
        speed = current_data.get('speed')

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
        """Required keys: 'rpm', 'speed', 'timestamp'."""
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

    def _create_schema(self, incident_type, current_data: dict, desc: str,
                       car_id: int) -> IncidentSchema:
        """
        Required keys: 'rpm', 'speed', 'timestamp', 'coolant_temp',
        'oil_temp',.
        """
        rpm = current_data.get('rpm')
        speed = current_data.get('speed')
        timestamp = datetime.fromtimestamp(current_data.get('timestamp'))
        coolant_temp = current_data.get('coolant_temp')
        oil_temp = current_data.get('oil_temp')
        engine_load = current_data.get('load')

        new_incident = IncidentSchema(incident_type, desc,
                                      timestamp, car_id, 0, 0)
        return new_incident

    def validate_frame(self, data: dict, car_id: int,
                       fuel_type: FuelType,
                       previous_state: dict) -> tuple[dict, dict]:
        new_incidents = []
        incidents = previous_state.get('incidents', {
                                        IncidentType.COLD_ENGINE: [],
                                        IncidentType.REDLINING: [],
                                        IncidentType.PEELING_OUT: []
                                        })

        if self._check_thrashing_cold_engine(data, fuel_type):
            desc = 'Katuje auto na zimnym'
            new_incidents.append((IncidentType.COLD_ENGINE, desc))
        else:
            incidents[IncidentType.COLD_ENGINE].clear()

        is_peeling_out, new_state = self._check_peeling_out(data,
                                                            previous_state,
                                                            fuel_type)
        if is_peeling_out:
            desc = 'Start z piskiem'
            new_incidents.append((IncidentType.PEELING_OUT, desc))
        else:
            incidents[IncidentType.PEELING_OUT].clear()

        if self._check_redlining(data, fuel_type):
            desc = 'Odcinka'
            new_incidents.append((IncidentType.REDLINING, desc))
        else:
            incidents[IncidentType.REDLINING].clear()

        res = {}
        for incident, desc in new_incidents:
            new_incident_schema = self._create_schema(incident, data,
                                                      desc, car_id)
            incidents[incident].append(new_incident_schema)

            if incident == IncidentType.PEELING_OUT or len(incidents[incident]) > 3:
                res[incident] = list(incidents[incident])
                incidents[incident].clear()

        new_state['incidents'] = incidents
        return res, new_state
