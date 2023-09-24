import redis
import json
import csv

r = redis.Redis(
  host='redis-16440.c302.asia-northeast1-1.gce.cloud.redislabs.com',
  port=16440,
  password='Sm33mynNsJZxG39Tbult6TenGv8C9GQU')

# sample_vehicles = [
#     {'id': 1, 'type': 'Electric Car', 'available': True},
#     {'id': 2, 'type': 'Electric Bus', 'available': False},
#     {'id': 3, 'type': 'Electric Bike', 'available': True},
# ]

# for vehicle_data in sample_vehicles:
#     r.hset(f'vehicle:{vehicle_data["id"]}', vehicle_data)


ELECTRIC_BUSES = ['K1','K3','K2A','K4','K2']
vehicles = []
# Define the file paths
for bus in ELECTRIC_BUSES :

    csv_file_path = 'elec_bus_details/'+bus+'.csv'  # Replace with the actual file path

    # Initialize an empty list to store the data
    data = []

    # Read the CSV file using DictReader
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter='\t')
        for row in csvreader:
            data.append(row)

    # Write the data to a JSON file


    for row in data:
        # print(row.get("STOPS"))

        value = row['STOPS,STOP NUMBER']

        # Split the value into stop name and stop number
        stop_name, stop_number = value.split(',')

        # Print the stop name and stop number
        # print(f'Stop Name: {stop_name}, Stop Number: {stop_number}')

        vehicles.append({'id_value': bus+stop_name ,'id': bus,'stop_name': stop_name,'stop_number':  stop_number,'type': 'Electric Bus', 'available': True})

# print(vehicles)



for vehicle_data in vehicles:
    r.hset(f'vehicle:{vehicle_data["id_value"]}', 'data', json.dumps(vehicle_data))

# raw_data = r.hget('vehicle:1', 'data')
# vehicle_data = json.loads(raw_data)
# print(vehicle_data)
