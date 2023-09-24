import redis
import json
import csv

r = redis.Redis(
  host='redis-16440.c302.asia-northeast1-1.gce.cloud.redislabs.com',
  port=16440,
  password='Sm33mynNsJZxG39Tbult6TenGv8C9GQU')

# print(r.keys())

keys = r.keys('vehicle:*')

stops= []

def get_fare(start,dest):
  start_num = 0
  dest_num = 0
  for key in keys:
    vehicle_data = r.hgetall(key)
    data = json.loads(vehicle_data[b'data'])
    if data['stop_name'] == start:
      start_num = int(data['stop_number'])
    if data['stop_name'] == dest:
      dest_num = int(data['stop_number'])
  return abs(start_num-dest_num)*3



# print (stops)
