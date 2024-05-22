#!/bin/bash

sudo docker pull influxdb:2.7.6

sudo docker run \
 --name influxdb2 \
 --publish 8086:8086 \
 --mount type=volume,source=influxdb2-data,target=/var/lib/influxdb2 \
 --mount type=volume,source=influxdb2-config,target=/etc/influxdb2 \
 --env DOCKER_INFLUXDB_INIT_MODE=setup \
 --env DOCKER_INFLUXDB_INIT_USERNAME=OussAtmo \
 --env DOCKER_INFLUXDB_INIT_PASSWORD=123plouf \
 --env DOCKER_INFLUXDB_INIT_ORG=AC \
 --env DOCKER_INFLUXDB_INIT_BUCKET=CNRS \
 influxdb:2

