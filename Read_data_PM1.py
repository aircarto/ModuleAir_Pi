#from influxdb import InfluxDBClient
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
#from  influx_variables import TOKEN, ORG, BUCKET, URL

TOKEN = "bfV4whBMLS2YO_pEx7ggE87V7Cw5zsPDhxJxf5DKJbLvbuo-fOjq_wsD1u8Zo164C1IQpsHDx1HiZjP5KwJpLw=="
ORG = "AC"
BUCKET = "CNRS"
URL="http://localhost:8086"
client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)

query_api = client.query_api()


with open('/var/www/html/ModuleAir_Pi/device_id.txt', 'r') as file:
   name = file.read().strip()

query = f"""
from(bucket: "CNRS")
    |> range(start: -2m)
    |> filter(fn: (r) => r["_measurement"] == "{name}")
    |> filter(fn: (r) => r["_field"] == "PM1")
    |> mean()
"""

tables = query_api.query(query, org="AC")

for table in tables:
    for record in table.records:
        value = record.values["_value"]
        x = round(value, 2)
        print(x)