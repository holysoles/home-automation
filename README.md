# home-automation
A python script set to run in the background on a Raspberry Pi to automate various things

launcher.sh --- bash script that is set with crontab to run on reset, launches mc.py with nohup in the background

mc.py --- main script, used to sub channel changes, currently coming through pubnub, which receives pub posts through IFTTT

samsung.conf --- backup LIRC config file for samsung tv infrared remote commands
