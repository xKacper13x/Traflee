from exceptions import MissingParams


class DepositValidator:
    def __init__(self):
        pass

    def _check_thrashing_cold_engine(self, coolant_temp, oil_temp,
                                     rpm, engine_load):
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

    def check_deposit_rules(self, data: dict) -> dict:
        coolant_temp = data.get('coolant_temp')
        oil_temp = data.get('oil_temp')
        rpm = data.get('rpm')
        load = data.get('load')

        res = {
            'status': True,
            'comment': 'Jazda prawidłowa'
        }

        try:
            if self._check_thrashing_cold_engine(coolant_temp, oil_temp,
                                                 rpm, load):
                res['status'] = False
                res['comment'] = "ALARM: Agresywna jazda na zimnym silniku (wysokie obciążenie/RPM)"
        except MissingParams:
            res['status'] = False
            res['comment'] = "BŁĄD: Brak wystarczających danych z czujników do oceny"

        return res
