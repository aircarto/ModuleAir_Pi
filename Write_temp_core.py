import random
import json
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import bme280
import psycopg2

with open('/var/www/html/ModuleAir_Pi/device_id.txt', 'r') as file:
   name = file.read().strip()

token = "BzPrvA1UzNPbDMC0iIgiVZ_XjKBswuYC1cfrG2_anGXU9b4cwDnpS6pAz_ToOpgYSlBl1O7C3VWgFFXX5x9cEA=="
org = "AC"
bucket = "CNRS"
url="http://localhost:8087"

with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
    temp_core = file.read()

temp_core = float(temp_core) / 1000


client = InfluxDBClient(url=url, token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)


point = Point(name) \
    .field("temperature_core", temp_core)

write_api.write(bucket=bucket, org=org, record=point)