import random
import json
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import bme280
import psycopg2
import smbus
import requests



token = "BzPrvA1UzNPbDMC0iIgiVZ_XjKBswuYC1cfrG2_anGXU9b4cwDnpS6pAz_ToOpgYSlBl1O7C3VWgFFXX5x9cEA=="
org = "AC"
bucket = "CNRS"
url="http://localhost:8087"

# with open('device_id.txt', 'r') as file:
   # name = file.read().strip()

name = CNRS_1

DEVICE1 = 0x76
DEVICE2 = 0x77
DEVICE3 = 0x76

def read_sensor_data1(address):
    bus = smbus.SMBus(1)
    temperature, pressure, humidity = bme280.readBME280All(address)
    return temperature, pressure, humidity

def read_sensor_data2(address):
    bus = smbus.SMBus(3)
    temperature, pressure, humidity = bme280.readBME280All(address)
    return temperature, pressure, humidity

temperature1, pressure1, humidity1 = read_sensor_data1(DEVICE1)
temperature2, pressure2, humidity2 = read_sensor_data1(DEVICE2)
temperature3, pressure3, humidity3 = read_sensor_data2(DEVICE3)

client = InfluxDBClient(url=url, token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)


point1 = Point(name) \
    .field("temperature1", temperature1) .field("pressure1", pressure1) .field("humidity1", humidity1) 

point2 = Point(name) \
    .field("temperature2", temperature2) .field("pressure2", pressure2) .field("humidity2", humidity2) 

point3 = Point(name) \
    .field("temperature3", temperature3) .field("pressure3", pressure3) .field("humidity3", humidity3) 

write_api.write(bucket=bucket, org=org, record=[point1, point2,point3])


url = 'https://webhook.site/4767a01a-0cc9-494a-a1f4-0860f9ce38af'

data = {
    "Name" : name,
    "Temperature1": temperature1,
    "Pressure1": pressure1,
    "Humidity1": humidity1,
    "Temperature2": temperature2,
    "Pressure2": pressure2,
    "Humidity2": humidity2,
    "Temperature3": temperature3,
    "Pressure3": pressure3,
    "Humidity3": humidity3
}

x = requests.post(url, json = data)


