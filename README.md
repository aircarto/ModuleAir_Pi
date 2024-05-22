# ModuleAir_Pi

ModuleAir-Pi est un projet porté par AirCarto : https://aircarto.fr/

# Explications

Le ModuleAir_Pi est un dispositif qui a vocation à déterminer l'impact de la qualité de l'air sur le ressenti, l'humeur, le bien-être etc
Pour se faire, le ModuleAir_PI propose une à plusieurs question fermés auxquels l'utilisateur doit répondre. Suite à cela, l'utilisateur est dirigé sur une page où des données tel que la temperature, le taux de CO2, le taux d'humidité ou encore le nombre de PM sont affichées. 

## Hardware

- Un raspberry PI 5 se charge de lancer les programmes, de receuillir les données, de faire le lien entre les capteurs et l'écran, d'afficher les questions etc
- Les questions et les données sont affichés sur un écran tactile de 7 pouces de résolution 1024x600 
- La temperature, l'humidité et la pression sont mesurés par une sonde BME280. Cette dernière est branchée au Raspberry sur les ports 3v-GND-SDA-SCL. La marge de précision des données est de 1°C. Les sondes BME sont au nombre de 3. Afin de gagner en précision, le ModuleAir_Pi calcule la moyenne de temperature, de pression et d'humidité remontées par les 3 BME. Cela permet également de prévenir d'une eventuelle anomalie. Si une sonde est défailante, la comparaison avec les 2 autres permet de la trouver.  
- Les PM sont mesurés par un capteur NextPM, connecté sur un port USB avec un convertisseur CH340. 
- Le CO2 est mesuré par une sonde mh-z19b
- Le tout est disposé dans un boîtier (c.f partie Boitier)

## Software

Différents modules sont nécessaires au fonctionnement du ModuleAire_Pi : 
- Apache2 pour le serveur web.
- PHP pour le front-end (développement des pages de questions et de données) avec composer. 
- Python pour le back-end (développement des scripts d'instructions d'écriture et de lecture de données).
- InfluxDB pour stocker les données recensées par les différents capteurs et sondes. 
- Docker pour le fonctionnement d'InfluxDB.
- Postgres pour stocker les réponses saisies par l'utilisateur (bien-être + données de temperature, pression etc au moment de sa réponse).

Ces differents modules peuvent être installés avec les commandes suivantes (un script install.sh permet de tout installer en une fois) : 
- Apache2 : sudo apt install apache2
- PHP : sudo apt install php
- composer:
- Pip : sudo apt install python3-pip
- Python : sudo apt install python3
- Serial : pip install pyserial
- InfluxDB : sudo curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add - | pip install influxdb-client
- Docker : https://docs.docker.com/engine/install/raspberry-pi-os/
- Postgres : sudo apt install postgresql postgresql-contrib
- Psycopg2 : pip install psycopg2-binary


## Fichier

- bme280.py : Permet le fonctionnement de la sonde BME280 et récolte les données de temperature, pression et humidité.
- Write_data_***.py : Inscrit les données recupérés par les différents capteurs et sondes sur InfluxDB.
- Read_data_***.py : Récupère les données depuis InfluxDB.
- reponse.php | index.html | questionX.html | style.css : affichent respectivement les pages web de questions et de données
- global.php : Donne l'identifiant du capteur (à créer pour chaque boîtier). Le nom est repercuté dans "device_id.txt", (qui est automatiquement crée par global.php)

```
<?php
define('DEVICE_ID', '`*nom que l'on veut donner au capteur*`');
file_put_contents('/var/www/html/ModuleAir_Pi/device_id.txt', DEVICE_ID); ?>
```

Remarque : Le fichier crontab (accessible via la commande crontab -e) doit être modifier de la sorte afin d'automatiser les processus : 
```

*/2 * * * * python /var/www/html/ModuleAir_Pi/Write_data_BME280.py
*/2 * * * * python /var/www/html/ModuleAir_Pi/Write_data_NextPM.py
*/2 * * * * python /var/www/html/ModuleAir_Pi/Write_Data_CO2.py
*/2 * * * * python /var/www/html/ModuleAir_Pi/Write_temp_core.py
0 9 * * * python /var/www/html/ModuleAir_Pi/csv_files/create_csv_sensors.py >> /var/www/html/ModuleAir_Pi/logs/app.log 2>&1
0 9 * * * python /var/www/html/ModuleAir_Pi/csv_files/create_csv_reponses.py >> /var/www/html/ModuleAir_Pi/logs/app.log 2>&1
@reboot /var/www/html/ModuleAir_Pi/app.sh
@reboot sudo php /var/www/html/ModuleAir_Pi/global.php

```

Pour prévenir des éventuels switch de port de la sonde de CO2 et NextPM, il faut respectivement créer un fichier CO2.rules et un fichier PM.rules au niveau de /etc/udev/rules.d/ :

CO2.rules

```
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="C02" 

```
PM.rules
```
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="NextPM"
```

Il faut également activer le port I2C avec la commande:
```
 sudo raspi-config
```
Ensuite il faut activer le deuxième port I2C en ajoutant ces lignes dans le fichier /boot/firmware/config.txt :
```
 # Uncomment some or all of these to enable the optional hardware interfaces
dtparam=i2c_arm=on
dtparam=i2s=on
dtparam=spi=on
dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24
dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=17,i2c_gpio_scl=27

```
## SQL database

Data from the form are stored inside a psql database structured as follow:

```
CREATE TABLE public.reponses_new (
reponse varchar(20) NULL,
temperature float8  NULL,
humidity float8  NULL,
date_reponse timestamp NULL,
pressure int4 NULL,
co2 int4 NULL,
pm1 float8 NULL,
pm25 float8 NULL,
pm10 float8 NULL,
device_id varchar(50) NULL,
temprature_core float8  NULL,
sexe varchar(15) NULL,
activites varchar(60) NULL,
r1 varchar(100) NULL,
r2 varchar(100) NULL,
r3 varchar(100) NULL,
r4 varchar(100) NULL,
r5 varchar(100) NULL,
r6 varchar(100) NULL,
r7 varchar(100) NULL,
r8 varchar(100) NULL,
r9 varchar(100) NULL,
r10 varchar(100) NULL,
r11 varchar(100) NULL,
r12 varchar(100) NULL,
r13 varchar(100) NULL,
r14 varchar(100) NULL,
r15 varchar(100) NULL,
r16 varchar(100) NULL,
r17 varchar(100) NULL,
r18 varchar(100) NULL,
r19 varchar(100) NULL,
r20 varchar(100) NULL,
r21 varchar(100) NULL,
r22 varchar(100) NULL,
r23 varchar(100) NULL,
r24 varchar(100) NULL,
r25 varchar(100) NULL,
r26 varchar(100) NULL,
r27 varchar(100) NULL,
r28 varchar(100) NULL,
r29 varchar(100) NULL,
r30 varchar(100) NULL
);
```



## Boitier


![alt text](Images/Boitier.jpg)
![alt text](Images/ModuleAir.jpg)
![alt text](Images/Raspberry.jpg)




## TODO

- Installation de la sonde CO2
- Réflexion autour du design final du boitier 
- Brancher le ModuleAir avec une alimentation 5 Volt - 8 ampères pour répondre aux besoin du boîtier étant gourmand en énérgie
