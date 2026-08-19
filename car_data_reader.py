import obd


class CarDataReader:
    def __init__(self):
        print('Connecting')
        self._connection = obd.OBD("/dev/rfcomm0")
        if self._connection.is_connected():
            print('sukces')
        else:
            print('Failed')

    @property
    def is_connected(self) -> bool:
        return self._connection.is_connected()

    @property
    def vin(self) -> str | None:
        if self.is_connected:
            vin_response = self._connection.query(obd.commands.VIN)
            if not vin_response.is_null():
                return str(vin_response.value)
        return None

    @property
    def bridge_voltage(self) -> float | None:
        if self.is_connected:
            elm_voltage_res = self._connection.query(obd.commands.ELM_VOLTAGE)
            if not elm_voltage_res.is_null():
                return elm_voltage_res.value.magnitude

    @property
    def distance_with_mil_on(self) -> float | None:
        if self.is_connected:
            mil_dist_res = self._connection.query(obd.commands.DISTANCE_W_MIL)
            if not mil_dist_res.is_null():
                return mil_dist_res.value.magnitude

    def get_diagnostic_codes(self) -> list:
        dtc_codes = []

        if self.is_connected:
            dtc_response = self._connection.query(obd.commands.GET_DTC)
            if not dtc_response.is_null():
                for code_tuple in dtc_response.value:
                    dtc_codes.append({
                        'code': code_tuple[0],
                        'description': code_tuple[1]
                    })

        return dtc_codes

    def get_current_metrics(self) -> dict:
        metrics = {
            'rpm': None,
            'load': None,
            'coolant_temp': None,
            'ecu_voltage': None
        }

        if not self.is_connected:
            return metrics

        rpm_res = self._connection.query(obd.commands.RPM)
        load_res = self._connection.query(obd.commands.ENGINE_LOAD)
        coolant_temp_res = self._connection.query(obd.commands.COOLANT_TEMP)
        ecu_voltage_res = self._connection.query(
            obd.commands.CONTROL_MODULE_VOLTAGE)

        if not rpm_res.is_null():
            metrics['rpm'] = rpm_res.value.magnitude

        if not load_res.is_null():
            metrics['load'] = load_res.value.magnitude

        if not coolant_temp_res.is_null():
            metrics['coolant_temp'] = coolant_temp_res.value.magnitude

        if not ecu_voltage_res.is_null():
            metrics['ecu_voltage'] = ecu_voltage_res.value.magnitude

        return metrics
