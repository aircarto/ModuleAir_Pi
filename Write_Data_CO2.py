import serial
import requests
import json
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

with open('device_id.txt', 'r') as file:
   name = file.read().strip()

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
print(CO2)

ser.close()

token = "BzPrvA1UzNPbDMC0iIgiVZ_XjKBswuYC1cfrG2_anGXU9b4cwDnpS6pAz_ToOpgYSlBl1O7C3VWgFFXX5x9cEA=="
org = "AC"
bucket = "CNRS"
url="http://localhost:8087"



client = InfluxDBClient(url=url, token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

point = Point(name) \
    .field("CO2", CO2)

write_api.write(bucket=bucket, org=org, record=point)