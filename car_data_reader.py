import obd


class CarDataReader:
    def __init__(self):
        print('Connecting')
        self._connection = obd.Async("/dev/rfcomm0")
        if not self.is_connected:
            raise ConnectionError('Could not connect to car')

        self._vin = None
        vin_response = self._connection.query(obd.commands.VIN)
        if not vin_response.is_null():
            self._vin = str(vin_response.value)

        self._connection.watch(obd.commands.ELM_VOLTAGE)
        self._connection.watch(obd.commands.DISTANCE_W_MIL)
        self._connection.watch(obd.commands.GET_DTC)
        self._connection.watch(obd.commands.RPM)
        self._connection.watch(obd.commands.ENGINE_LOAD)
        self._connection.watch(obd.commands.COOLANT_TEMP)
        self._connection.watch(obd.commands.CONTROL_MODULE_VOLTAGE)
        self._connection.start()

    @property
    def is_connected(self) -> bool:
        return self._connection.is_connected()

    @property
    def vin(self) -> str | None:
        return self._vin

    @property
    def bridge_voltage(self) -> float | None:
        if not self.is_connected:
            raise ConnectionAbortedError('Connection lost during runtime')

        elm_voltage_res = self._connection.query(obd.commands.ELM_VOLTAGE)
        if not elm_voltage_res.is_null():
            return elm_voltage_res.value.magnitude

    @property
    def distance_with_mil_on(self) -> float | None:
        if not self.is_connected:
            raise ConnectionAbortedError('Connection lost during runtime')

        mil_dist_res = self._connection.query(obd.commands.DISTANCE_W_MIL)
        if not mil_dist_res.is_null():
            return mil_dist_res.value.magnitude

    def get_diagnostic_codes(self) -> list:
        dtc_codes = []

        if not self.is_connected:
            raise ConnectionAbortedError('Connection lost during runtime')

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
            raise ConnectionAbortedError('Connection lost during runtime')

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
