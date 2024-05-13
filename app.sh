#!/bin/sh

sleep 15

export DISPLAY=:0

pkill chromium

sleep 5

# Version fullscreen: 
chromium-browser --start-fullscreen http://localhost:55555
