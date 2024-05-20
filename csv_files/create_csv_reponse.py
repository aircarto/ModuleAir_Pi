'''
Python script
create a CSV file from the data stored locally by influxdb
send it to aircarto server with rsync
'''

import csv
import subprocess
import psycopg2
from psycopg2 import sql
import decimal


from datetime import datetime

print("Save measures to .csv file and send it to aircarto server")
with open('/var/www/html/ModuleAir_Pi/device_id.txt', 'r') as file:
   name = file.read().strip()

db_config = {
    'dbname': 'cnrs',
    'user': 'airlab_test',
    'password': '123plouf',
    'host': 'localhost',
    'port': '5432'
}

data_type = "reponses"
filename = f"/var/www/html/ModuleAir_Pi/csv_files/{name}_{data_type}.csv"

def convert_decimal(value):
    if isinstance(value, decimal.Decimal):
        return float(value)
    return value

try:
    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    # Execute a query
    query = "SELECT * FROM reponses_new;"
    cursor.execute(query)

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Get column names from the cursor description
    colnames = [desc[0] for desc in cursor.description]

    # Specify the CSV file name
    csv_file_name = filename

    # Write the data to a CSV file
    with open(csv_file_name, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the column names as the header
        csv_writer.writerow(colnames)

        # Convert rows and write them
        for row in rows:
            formatted_row = [convert_decimal(value) for value in row]
            csv_writer.writerow(formatted_row)

    print(f"Data has been written to {csv_file_name}")

except Exception as error:
    print(f"Error: {error}")

finally:
    # Close the database connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")







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
