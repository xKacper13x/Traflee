from app.database.crud import incident
from app.services.car_data_reader import CarDataReader
from app.services.deposit_validator import DepositValidator
from app.services.dtc_translator import DTCTranslator
from app.database.db_config import engine, Session
import app.database.models as models
from app.database.crud import rental, dtc_code
from app.core.enums import FuelType
from app.database.schemas import DTCCodeSchema
import time


models.Base.metadata.create_all(engine)
session = Session()

rental.add(session, 'Pierwsza Wypozyczalnia')

deposit_validator = DepositValidator()

is_connected = False
while not is_connected:
    try:
        data_reader = CarDataReader()
    except ConnectionError:
        time.sleep(3)
        continue
    is_connected = True
    print('Connected properly')

time.sleep(3)
running = True
prev_state = {'was_stationary': True}

fuel_type = FuelType.PETROL
car_profile = 'Samochód miejski'
car_brand = 'Audi'
i = 1
while running:
    try:
        dtc_codes = data_reader.get_diagnostic_codes()
        car_data = data_reader.get_current_metrics()
    except ConnectionAbortedError as e:
        print(e)
        running = False
        continue

    for error in dtc_codes:
        code = error['code']
        raw_description = error['description']
        print('Błąd')
        # cała kolejność to najpierw redis, potem SQL,
        # potem znowu pytanie do redisa czy już zapytal AI
        # i potem pytanie do AI
        code_in_base = dtc_code.find_dtc_translation(session, code,
                                                     car_profile,
                                                     car_brand, fuel_type)
        if code_in_base is not None and code_in_base.is_verified:
            print(f'severity: {code_in_base.severity}\nmanager_explanation: {code_in_base.manager_explanation}\naction_required: {code_in_base.action_required}')
        else:
            translator = DTCTranslator()
            response = translator.analyze_error(code, raw_description,
                                                   fuel_type, car_profile,
                                                   car_brand)
            print(f'severity: {response.severity.value}\nmanager_explanation: {response.manager_explanation}\naction_required: {response.action_required}')
            new_code = DTCCodeSchema(code=code, car_type=car_profile, car_brand=car_brand,
                                     fuel_type=fuel_type, severity=response.severity,
                                     manager_explanation=response.manager_explanation,
                                     action_required=response.action_required,
                                     is_verified=False)
            dtc_code.add(session, new_code)

    result, is_stationary = deposit_validator.validate_frame(car_data, 1,
                                                             FuelType.PETROL,
                                                             prev_state)
    prev_state['was_stationary'] = is_stationary

    for incident_type, schemas_list in result.items():
        incident.add(session, schemas_list[0])
        print(f'{i}. New incident added: {incident_type}')
        i += 1
    time.sleep(0.5)


# with open('None_data.csv', 'r') as file_handle:
#     reader = csv.DictReader(file_handle)
#     car_data = {
#         'rpm': None,
#         'load': None,
#         'coolant_temp': None
#     }
#     for row in reader:
#         car_data['rpm'] = float(row['RPM'])
#         car_data['load'] = float(row['load'])
#         car_data['coolant_temp'] = row.get('coolant_temp', 20)
#         res = deposit_validator.check_deposit_rules(car_data)

session.close()
