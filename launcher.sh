#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
sudo python /home/pi/automation/heater/repair.py &
sudo nohup python /home/pi/automation/mc.py &
cd /

