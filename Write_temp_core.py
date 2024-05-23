import random
import json
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import bme280
import psycopg2
#from  influx_variables import TOKEN, ORG, BUCKET, URL

TOKEN = "bfV4whBMLS2YO_pEx7ggE87V7Cw5zsPDhxJxf5DKJbLvbuo-fOjq_wsD1u8Zo164C1IQpsHDx1HiZjP5KwJpLw=="
ORG = "AC"
BUCKET = "CNRS"
URL="http://localhost:8086"

with open('/var/www/html/ModuleAir_Pi/device_id.txt', 'r') as file:
   name = file.read().strip()



with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
    temp_core = file.read()

temp_core = float(temp_core) / 1000


client = InfluxDBClient(url=URL, token=TOKEN)
write_api = client.write_api(write_options=SYNCHRONOUS)


point = Point(name) \
    .field("temperature_core", temp_core)

write_api.write(bucket=BUCKET, org=ORG, record=point)