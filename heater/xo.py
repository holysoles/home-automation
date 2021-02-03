#Script for heater on/off

import serial 
import sys

tdata= "xo00"
   
port = serial.Serial("/dev/rfcomm0", baudrate=9600)
while True:
 print "SENDING..."
 port.write(tdata)
 rcv = port.readline()
 if rcv:
  print(rcv)
  sys.exit("done")
