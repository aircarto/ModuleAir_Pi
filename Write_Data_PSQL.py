import subprocess
import time
import psycopg2

def execute_python_script(script_path):
    return subprocess.run(['python', script_path], capture_output=True, text=True).stdout.strip()


def get_device_id(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()

device_id = get_device_id("/var/www/html/ModuleAir_Pi/device_id.txt")

temperature = execute_python_script("/var/www/html/ModuleAir_Pi/Read_data_temp.py")
humidity = execute_python_script("/var/www/html/ModuleAir_Pi/Read_data_hum.py")
pressure = execute_python_script("/var/www/html/ModuleAir_Pi/Read_data_press.py")
pm1 = execute_python_script("/var/www/html/ModuleAir_Pi/Read_data_PM1.py")
pm25 = execute_python_script("/var/www/html/ModuleAir_Pi/Read_data_PM25.py")
pm10 = execute_python_script("/var/www/html/ModuleAir_Pi/Read_data_PM10.py")


with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
    temp_core = float(file.read().strip()) / 1000


full_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
rounded_pressure = round(float(pressure))


conn = psycopg2.connect(host="localhost", dbname="cnrs", user="airlab_test", password="123plouf")
cur = conn.cursor()


query = """
    INSERT INTO reponses (
        temperature, humidity, date_reponse, pressure, device_id, temprature_core, pm1, pm25, pm10
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
data = (temperature, humidity, full_date, rounded_pressure, device_id, temp_core, pm1, pm25, pm10)


cur.execute(query, data)
conn.commit()
cur.close()
conn.close()