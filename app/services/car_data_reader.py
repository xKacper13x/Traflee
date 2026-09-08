import obd
import time


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
        # self._connection.watch(obd.commands.GET_PENDING_DTC)
        self._connection.watch(obd.commands.RPM)
        self._connection.watch(obd.commands.SPEED)
        self._connection.watch(obd.commands.ACCELERATOR_POS_D)
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
        # pendind_dtc_response = self._connection.query(obd.commands.GET_PENDING_DTC)
        print(len(dtc_response.value))
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
            'speed': None,
            'throttle_pos': None,
            'load': None,
            'coolant_temp': None,
            'oil_temp': None,
            'ecu_voltage': None
        }

        if not self.is_connected:
            raise ConnectionAbortedError('Connection lost during runtime')

        rpm_res = self._connection.query(obd.commands.RPM)
        speed_res = self._connection.query(obd.commands.SPEED)
        throttle_pos_res = self._connection.query(obd.commands.ACCELERATOR_POS_D)
        load_res = self._connection.query(obd.commands.ENGINE_LOAD)
        coolant_temp_res = self._connection.query(obd.commands.COOLANT_TEMP)
        oil_temp_res = self._connection.query(obd.commands.OIL_TEMP)
        ecu_voltage_res = self._connection.query(
            obd.commands.CONTROL_MODULE_VOLTAGE)

        if not rpm_res.is_null():
            metrics['rpm'] = rpm_res.value.magnitude

        if not speed_res.is_null():
            metrics['speed'] = speed_res.value.magnitude

        if not throttle_pos_res.is_null():
            metrics['throttle_pos'] = throttle_pos_res.value.magnitude

        if not load_res.is_null():
            metrics['load'] = load_res.value.magnitude

        if not coolant_temp_res.is_null():
            metrics['coolant_temp'] = coolant_temp_res.value.magnitude

        if not oil_temp_res.is_null():
            metrics['oil_temp'] = oil_temp_res.value.magnitude

        if not ecu_voltage_res.is_null():
            metrics['ecu_voltage'] = ecu_voltage_res.value.magnitude

        return metrics

    def clear_diagnostic_codes(self) -> bool:
        """Wysyła żądanie skasowania kodów DTC ze sterownika."""
        if not self.is_connected:
            raise ConnectionAbortedError('Connection lost during runtime')

        print("Wysyłam żądanie skasowania błędów (Mode 04)...")
        # CLEAR_DTC zawsze ma response.value == None w python-obd, więc nie sprawdzamy is_null()
        self._connection.query(obd.commands.CLEAR_DTC)

        time.sleep(2)
        # Sprawdzamy stan po kasowaniu:
        remaining_errors = self.get_diagnostic_codes()
        if len(remaining_errors) == 0:
            print("Sukces! Pamięć błędów wyczyszczona.")
            return True
        else:
            print(f"Błędy nadal obecne w pamięci ({len(remaining_errors)}).")
            return False
