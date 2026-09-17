from app.services.car_data_reader import CarDataReader
from app.database.db_config import engine, Session
from app.database.crud import incident, dtc_code, car
from app.core.fleet_monitor import FleetMonitor
import app.database.models as models
import time


models.Base.metadata.create_all(engine)
session = Session()

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
fleet_monitor = FleetMonitor(session)

current_car = car.get_by_id(session, 1)

while running:
    try:
        new_metrics = data_reader.get_current_metrics()
        codes = data_reader.get_diagnostic_codes()
    except ConnectionAbortedError:
        print('Lost connection')
        time.sleep(3)

    result = fleet_monitor.run_cycle(current_car, new_metrics,
                                     codes)
    codes_translation, codes_to_save, new_incidents = result

    for code_to_save in codes_to_save:
        dtc_code.add(session, code_to_save)

    for incident_type, schemas_list in new_incidents.items():
        incident.add(session, schemas_list[0])

    time.sleep(0.5)

session.close()
