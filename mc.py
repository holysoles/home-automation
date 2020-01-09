#a Python script for automating my media center with a dc-dc relay for N64, 
#relay power strip for stereo and hyperion backlight, and ir commands 
#for tv power and other commands

#shebang line goes here

#Import all the libraries
import RPi.GPIO as GPIO
import os
import time
import serial 
from pubnub import Pubnub
 
# Initialize the Pubnub Keys
pub_key = "pub-c-1d7fb54e-2098-4ee4-9dcb-8a18f7ed6686"
sub_key = "sub-c-f4ed3de6-2821-11ea-9e12-76e5f2bf83fc"
 
# Define GPIO pins
STRIP = 21
N64RST = 2
N6433 = 3
N6412 = 4

def init(): #initalize the pubnub keys and start subscribing
 
 #Pubnub Initialization
 global pubnub
 pubnub = Pubnub(publish_key=pub_key,subscribe_key=sub_key)
 pubnub.subscribe(channels='automation', callback=callback, error=callback, reconnect=reconnect, disconnect=disconnect)

 #GPIO Initialization
 GPIO.setmode(GPIO.BCM)
 GPIO.setwarnings(False)
 GPIO.setup(N64RST,GPIO.OUT)
 GPIO.output(N64RST, True) 
 GPIO.setup(N6412,GPIO.OUT)
 GPIO.output(N6412, True) 
 GPIO.setup(N6433,GPIO.OUT)
 GPIO.output(N6433, True)
 GPIO.setup(STRIP,GPIO.OUT)
 GPIO.output(STRIP, True)
 
def controls(controlCommand): #this function listens for each trigger and executes accordingly
 if(controlCommand.has_key("trigger")):
  if(controlCommand["trigger"] == "center_on"):
   GPIO.output(STRIP, True)
   time.sleep(0.5)
   os.system('sudo service hyperion start')
   os.system('irsend SEND_ONCE samsung KEY_POWER')
   print "Power Strip Relay Activated and TV on"
  if(controlCommand["trigger"] == "center_off"):
   os.system('irsend SEND_ONCE samsung KEY_POWER')
   time.sleep(0.1)
   GPIO.output(STRIP, False)
   os.system('sudo service hyperion stop')
   print "Power Strip Relay Deactivated and TV off"
  if(controlCommand["trigger"] == "n64_on"):
   GPIO.output(N6433, False)
   GPIO.output(N6412, False)
   os.system('irsend SEND_ONCE samsung KEY_1')
   time.sleep(0.3)
   os.system('irsend SEND_ONCE samsung KEY_RIGHT')
   time.sleep(0.1)
   os.system('irsend SEND_ONCE samsung KEY_ENTER')
   print "Nintendo 64 was switched on"
  if(controlCommand["trigger"] == "n64_off"):
   GPIO.output(N6433, True)
   GPIO.output(N6412, True)
   os.system('irsend SEND_ONCE samsung KEY_1')
   time.sleep(0.3)
   os.system('irsend SEND_ONCE samsung KEY_LEFT')
   time.sleep(0.1)
   os.system('irsend SEND_ONCE samsung KEY_ENTER')
   print "Nintendo 64 was switched off"
  if(controlCommand["trigger"] == "n64_reset"):
   GPIO.output(N64RST, False)
   time.sleep(0.5)
   GPIO.output(N64RST, True)
   print "Nintendo 64 was Reset"
  if(controlCommand["trigger"] == "tv"):
   os.system('irsend SEND_ONCE samsung KEY_1')
   time.sleep(0.3)
   os.system('irsend SEND_ONCE samsung KEY_LEFT')
   time.sleep(0.1)
   os.system('irsend SEND_ONCE samsung KEY_ENTER')
   print "Input switched to TV"
  if(controlCommand["trigger"] == "netflix"):
   os.system('irsend SEND_ONCE samsung KEY_5')
   time.sleep(0.6)
   os.system('irsend SEND_ONCE samsung KEY_RIGHT')
   time.sleep(0.1)
   os.system('irsend SEND_ONCE samsung KEY_ENTER')
   print "Netflix was launched"
  if(controlCommand["trigger"] == "hdmi"):
   os.system('irsend SEND_ONCE samsung KEY_1')
   time.sleep(0.3)
   os.system('irsend SEND_ONCE samsung KEY_RIGHT')
   time.sleep(0.1)
   os.system('irsend SEND_ONCE samsung KEY_ENTER')
   print "Input Switched to HDMI"
  if("input" in controlCommand["trigger"]):
   longstring =  controlCommand["trigger"]
   shortstring = longstring.replace("input_", "")
   inputcount = int(shortstring)
   os.system('irsend SEND_ONCE samsung KEY_1')
   time.sleep(0.3) 
   for i in range(0, inputcount):
    os.system('irsend SEND_ONCE samsung KEY_RIGHT')
    time.sleep(0.1)
   os.system('irsend SEND_ONCE samsung KEY_ENTER')
   print "Input switched!"
  if(controlCommand["trigger"] == "tvpwr"):
   os.system('irsend SEND_ONCE samsung KEY_POWER')
   print "TV power command sent"  
  
  #heater commands
  if(controlCommand["trigger"] == "temperature"): 
   val = controlCommand["status"]
   tdata = "xd" + val
   port = serial.Serial("/dev/rfcomm0", baudrate=9600)
   while True:
    print "SENDING..."
    port.write(tdata)
    rcv = port.readline()
    if rcv:
     print(rcv)
     break
  if(controlCommand["trigger"] == "timer"):
   val = controlCommand["status"]
   tdata = "xt" + val
   port = serial.Serial("/dev/rfcomm0", baudrate=9600)
   while True:
    print "SENDING..."
    port.write(tdata)
    rcv = port.readline()
    if rcv:
     print(rcv)
  if(controlCommand["trigger"] == "heaterpwr"): 
   os.system('sudo python /home/pi/automation/heater/xo.py')  
  if(controlCommand["trigger"] == "preheat"):
    os.system('sudo python /home/pi/automation/heater/xp.py')
 else:
  pass
 
 
# the following function listens for a message on the channel with a requester
# identifier, then executes the controls function
def callback(message, channel):
 if(message.has_key("requester")):
  controls(message)
 else:
  pass
 
 
def error(message): #if there is error in the channel,print the error
 print("ERROR : " + str(message))
 
 
def reconnect(message): #responds if server connects with pubnub
 print("RECONNECTED")
 
 
def disconnect(message): #responds if server disconnects with pubnub
 print("DISCONNECTED")
 
 
if __name__ == '__main__':
 init() #Initialize the Script
