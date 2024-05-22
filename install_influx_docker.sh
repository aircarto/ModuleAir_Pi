#!/bin/bash

sudo docker pull influxdb:latest

docker run -d \
  --name influxdb \
  -p 8087:8087 \
  -v $PWD/influxdb:/var/lib/influxdb2 \
  influxdb:latest
