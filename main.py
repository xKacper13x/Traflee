from car_data_reader import CarDataReader
from deposit_validator import DepositValidator
from database.config import engine, Session
import database.models as models
import csv


models.Base.metadata.create_all(engine)

deposit_validator = DepositValidator()
# data_reader = CarDataReader()
running = True

# vin = data_reader.vin

# while running:
#     car_data = data_reader.get_current_metrics()
#     result = deposit_validator.check_deposit_rules(car_data)
#     print(result['comment'])


with open('None_data.csv', 'r') as file_handle:
    reader = csv.DictReader(file_handle)
    car_data = {
        'rpm': None,
        'load': None,
        'coolant_temp': None
    }
    for row in reader:
        car_data['rpm'] = float(row['RPM'])
        car_data['load'] = float(row['load'])
        car_data['coolant_temp'] = row.get('coolant_temp', 20)
        res = deposit_validator.check_deposit_rules(car_data)
        print(res['comment'])
