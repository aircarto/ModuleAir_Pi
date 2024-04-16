from influxdb import InfluxDBClient
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from statistics import mean 

token = "BzPrvA1UzNPbDMC0iIgiVZ_XjKBswuYC1cfrG2_anGXU9b4cwDnpS6pAz_ToOpgYSlBl1O7C3VWgFFXX5x9cEA=="
org = "AC"
bucket = "CNRS"
url="http://localhost:8087"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


query_api = client.query_api()

with open('device_id.txt', 'r') as file:
   name = file.read().strip()

query = f"""
from(bucket: "CNRS")
    |> range(start: -10)
    |> filter(fn: (r) => r["_measurement"] == "{name}" and (r["_field"] == "pressure1" or r["_field"] == "pressure2" or r["_field"] == "pressure3"))
      |> mean()
"""

tables = query_api.query(query, org="AC")

valeurs = []

for table in tables:
    for record in table.records:
        value = record.values ["_value"]
        x = round(value, 2)
        valeurs.append(x)

y = (mean(valeurs))
z = round(y, 2)
print(z)
