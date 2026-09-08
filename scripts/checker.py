from app.services.car_data_reader import CarDataReader
import time


is_connected = False
while not is_connected:
    try:
        data_reader = CarDataReader()
    except ConnectionError:
        time.sleep(3)
        continue
    is_connected = True
    print('Connected properly')

time.sleep(2)

try:
    car_data = data_reader.get_current_metrics()
except ConnectionAbortedError as e:
    print(e)

print(f'VIN : {data_reader.vin}')
print(f'Bridge voltage : {data_reader.bridge_voltage}')

for key, value in car_data.items():
    print(f'{key} : {value}')
