'''
Python script
create a CSV file from the data stored locally by influxdb
send it to aircarto server with rsync
'''

import csv
import subprocess
import psycopg2
from psycopg2 import sql

from datetime import datetime

print("Save measures to .csv file and send it to aircarto server")
with open('/var/www/html/ModuleAir_Pi/device_id.txt', 'r') as file:
   name = file.read().strip()

db_config = {
    'dbname': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port'
}

try:
    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    # Execute a query
    query = "SELECT * FROM reponses;"
    cursor.execute(query)

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Process the retrieved data
    for row in rows:
        print(row)

except Exception as error:
    print(f"Error: {error}")

finally:
    # Close the database connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

data_type = "reponses"
filename = f"/var/www/html/ModuleAir_Pi/csv_files/{name}_{data_type}.csv"
