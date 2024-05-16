from influxdb import InfluxDBClient
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "BzPrvA1UzNPbDMC0iIgiVZ_XjKBswuYC1cfrG2_anGXU9b4cwDnpS6pAz_ToOpgYSlBl1O7C3VWgFFXX5x9cEA=="
org = "AC"
bucket = "Test"
url="http://localhost:8087"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


query_api = client.query_api()

with open('/var/www/html/ModuleAir_Pi/device_id.txt', 'r') as file:
   name = file.read().strip()

query = f"""
from(bucket: "CNRS")
    |> range(start: -2m)
    |> filter(fn: (r) => r["_measurement"] == "{name}")
      |> filter(fn: (r) => r["_field"] == "PM10")
      |> mean()"""

tables = query_api.query(query, org="AC")

for table in tables:
    for record in table.records:
        value = record.values["_value"]
        x = round(value, 2)
        print(x)