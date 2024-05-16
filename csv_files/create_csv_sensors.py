'''
Python script
create a CSV file from the data stored locally by influxdb
send it to aircarto server with rsync
'''

import csv
import subprocess

from datetime import datetime
from influxdb import InfluxDBClient
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

print("Save measures to .csv file and send it to aircarto server")

token = "BzPrvA1UzNPbDMC0iIgiVZ_XjKBswuYC1cfrG2_anGXU9b4cwDnpS6pAz_ToOpgYSlBl1O7C3VWgFFXX5x9cEA=="
org = "AC"
bucket = "CNRS"
url="http://localhost:8087"

# Initialize InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)

with open('/var/www/html/ModuleAir_Pi/device_id.txt', 'r') as file:
   name = file.read().strip()


# Define the query
query = f"""
from(bucket: "CNRS")
    |> range(start: -300d, stop: now())
    |> filter(fn: (r) => r["_measurement"] == "{name}")
    |> filter(fn: (r) => r["_field"] == "PM1" 
        or r["_field"] == "PM10" 
        or r["_field"] == "PM25" 
        or r["_field"] == "CO2" 
        or r["_field"] == "humidity1"
        or r["_field"] == "humidity2"
        or r["_field"] == "humidity3"
        or r["_field"] == "pressure1"
        or r["_field"] == "pressure2"
        or r["_field"] == "pressure3"
        or r["_field"] == "temperature1"
        or r["_field"] == "temperature2"
        or r["_field"] == "temperature3"
         )
    |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> yield(name: "mean")

      """

# Execute the query
tables = client.query_api().query(query, org=org)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") #date and time
data_type = "measures"
filename = f"{name}_{data_type}_{timestamp}.csv"  
filename = f"/var/www/html/ModuleAir_Pi/csv_files/{name}_{data_type}.csv"

# Open a CSV file for writing
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(["time", "id", "PM1", "PM25","PM10","CO2","temp1","temp2","temp3","press1","press2","press3","hum1","hum2","hum3",])
    
    # Write the data rows
    for table in tables:
        print(table)
        for record in table.records:
            #print(record.get_time(), record.get_measurement(), record['PM1'])
            writer.writerow([
                record.get_time(), 
                record.get_measurement(),
                round(record['PM1'],2),
                round(record['PM25'],2),
                round(record['PM10'],2),
                round(record['CO2'],2),
                round(record['humidity1'],2),
                round(record['humidity2'],2),
                round(record['humidity3'],2),
                round(record['pressure1'],2),
                round(record['pressure2'],2),
                round(record['pressure3'],2),
                round(record['temperature1'],2),
                round(record['temperature2'],2),
                round(record['temperature3'],2)
                ])
print("Data successfully written to CSV file.")

# Close the InfluxDB client
client.close()

#send to aircarto server
# Define the local file/directory and remote server details
local_path = f"{filename}"
remote_user = 'debian'
remote_host = 'data.moduleair.fr'
remote_path = '/var/www/data.moduleair.fr/cnrs_biblio/csv_rsync/'

# Construct the rsync command
rsync_command = f"rsync -avz --recursive {local_path} {remote_user}@{remote_host}:{remote_path}"

# Execute the rsync command
try:
    subprocess.run(rsync_command, shell=True, check=True)
    print(f"Files have been successfully synchronized to {remote_user}@{remote_host}:{remote_path}")
except subprocess.CalledProcessError as e:
    print(f"Failed to synchronize files. Error: {e}")