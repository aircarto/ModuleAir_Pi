import serial
import requests
import json
import logging
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
#from  influx_variables import TOKEN, ORG, BUCKET, URL

TOKEN = "bfV4whBMLS2YO_pEx7ggE87V7Cw5zsPDhxJxf5DKJbLvbuo-fOjq_wsD1u8Zo164C1IQpsHDx1HiZjP5KwJpLw=="
ORG = "AC"
BUCKET = "CNRS"
URL="http://localhost:8086"

with open('/var/www/html/ModuleAir_Pi/device_id.txt', 'r') as file:
   name = file.read().strip()

#logging.basicConfig(filename='/var/www/html/ModuleAir_Pi/logs/app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#logging.warning(f"Getting CO2 for: {name}")

ser = serial.Serial(
    port='/dev/C02',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 2
)

#ser.write(b'\x81\x11\x6E')      #data10s
ser.write(b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79')      #data60s

byte_data = ser.readline()
print(byte_data)
HIGH = int.from_bytes(byte_data[2:3], byteorder='big')
LOW = int.from_bytes(byte_data[3:4], byteorder='big')

CO2 = HIGH * 256 + LOW
print(str(CO2) + " PPM")
print("Device: " + name)

ser.close()


client = InfluxDBClient(url=URL, token=TOKEN)
write_api = client.write_api(write_options=SYNCHRONOUS)

point = Point(name) \
    .field("CO2", CO2)

write_api.write(bucket=BUCKET, org=ORG, record=point)

urlp = 'https://data.moduleair.fr/cnrs_biblio/data_cron.php'

data = {
    "Name" : name,
    "Type": "CO2",
    "CO2": CO2,
}

x = requests.post(urlp, json = data)