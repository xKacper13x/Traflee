from car_data_reader import CarDataReader
from deposit_validator import DepositValidator
from database.db_config import engine, Session
import database.models as models
from database.crud import rental, incident
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

running = True
while running:
    try:
        car_data = data_reader.get_current_metrics()
    except ConnectionAbortedError as e:
        print(e)
        running = False
        continue

    result = deposit_validator.check_deposit_rules(car_data)

    if not result['status']:
        incident.add(session, result['schemas'][0])
        print('New incident added')
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
