from car_data_reader import CarDataReader
from deposit_validator import DepositValidator
from database.db_config import engine, Session
import database.models as models
from database.crud import rental, incident
from database.schemas import IncidentSchema, CarSchema, UserSchema
import csv


models.Base.metadata.create_all(engine)
session = Session()

rental.add(session, 'Pierwsza Wypozyczalnia')

deposit_validator = DepositValidator()
# data_reader = CarDataReader()

# running = True
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

        if not res['status']:
            incident.add(session, res['schemas'][0])

session.close()
