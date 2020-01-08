#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
sudo nohup python /home/pi/automation/mc.py &
cd /

