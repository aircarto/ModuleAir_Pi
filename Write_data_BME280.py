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



client = InfluxDBClient(url=url, token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

temperature, pressure, humidity = bme280.readBME280All()

point = Point(name) \
    .field("temperature", temperature) .field("pressure", pressure) .field("humidity", humidity) 


write_api.write(bucket=bucket, org=org, record=point)
