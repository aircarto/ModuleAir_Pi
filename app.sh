#!/bin/sh

sleep 120

export DISPLAY=:0

pkill chromium

sleep 5

# Version fullscreen: 
#chromium-browser --start-fullscreen http://localhost --disable-pinch --no-user-gesture-required --overscroll-history-navigation=0 --disable-infobars --disable-restore-session-state --noerrdialogs --incognito

# Version kios: 
chromium-browser --kiosk --disable-infobars --disable-restore-session-state --noerrdialogs --incognito http://localhost
