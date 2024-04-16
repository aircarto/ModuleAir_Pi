import serial
import requests
import json
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 2
)

#ser.write(b'\x81\x11\x6E')      #data10s
ser.write(b'\x81\x12\x6D')      #data60s

while True:
    try:
        byte_data = ser.readline()
        print(byte_data)
        stateByte = int.from_bytes(byte_data[2:3], byteorder='big')
        Statebits = [int(bit) for bit in bin(stateByte)[2:].zfill(8)]
        PM1 = int.from_bytes(byte_data[9:11], byteorder='big')/10
        PM25 = int.from_bytes(byte_data[11:13], byteorder='big')/10
        PM10 = int.from_bytes(byte_data[13:15], byteorder='big')/10
        print(f"State: {Statebits}")
        print(f"PM1: {PM1}")
        print(f"PM25: {PM25}")
        print(f"PM10: {PM10}")
        #create JSON
        data = {
            'capteurID': 'nebuleairpro1',
            'sondeID':'USB2',
            'PM1': PM1,
            'PM25': PM25,
            'PM10': PM10,
            'sleep' : Statebits[0],
            'degradedState' : Statebits[1],
            'notReady' : Statebits[2],
            'heatError' : Statebits[3],
            't_rhError' : Statebits[4],
            'fanError' : Statebits[5],
            'memoryError' : Statebits[6],
            'laserError' : Statebits[7]
        }
        json_data = json.dumps(data)
        print(json_data)
        break
    except KeyboardInterrupt:
        print("User interrupt encountered. Exiting...")
        time.sleep(3)
        exit()
    except:
        # for all other kinds of error, but not specifying which one
        print("Unknown error...")
        time.sleep(3)
        exit()

# Write Data on Influx

# with open('device_id.txt', 'r') as file:
    # name = file.read().strip()

name = "CNRS_1"

token = "BzPrvA1UzNPbDMC0iIgiVZ_XjKBswuYC1cfrG2_anGXU9b4cwDnpS6pAz_ToOpgYSlBl1O7C3VWgFFXX5x9cEA=="
org = "AC"
bucket = "CNRS"
url="http://localhost:8087"



client = InfluxDBClient(url=url, token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

point = Point(name) \
    .field("PM1", PM1) .field("PM25", PM25) .field("PM10", PM10) 


write_api.write(bucket=bucket, org=org, record=point)
