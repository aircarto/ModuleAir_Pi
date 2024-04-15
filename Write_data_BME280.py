import random
import json
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import bme280
import psycopg2

name = "Capteur_1"

token = "BzPrvA1UzNPbDMC0iIgiVZ_XjKBswuYC1cfrG2_anGXU9b4cwDnpS6pAz_ToOpgYSlBl1O7C3VWgFFXX5x9cEA=="
org = "AC"
bucket = "CNRS"
url="http://localhost:8087"

DEVICE1 = 0x76
DEVICE2 = 0x77

def read_sensor_data(address):
    temperature, pressure, humidity = bme280.readBME280All(address)
    return temperature, pressure, humidity

temperature1, pressure1, humidity1 = read_sensor_data(DEVICE1)
temperature2, pressure2, humidity2 = read_sensor_data(DEVICE2)

client = InfluxDBClient(url=url, token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)


point1 = Point(name) \
    .field("temperature1", temperature1) .field("pressure1", pressure1) .field("humidity1", humidity1) 

point2 = Point(name) \
    .field("temperature2", temperature2) .field("pressure2", pressure2) .field("humidity2", humidity2) 

write_api.write(bucket=bucket, org=org, record=[point1, point2])
