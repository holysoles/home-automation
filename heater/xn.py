#Script for heater night temp change

import serial 
import sys

tdata= "xn00"
   
port = serial.Serial("/dev/rfcomm0", baudrate=9600)
while True:
 print "SENDING..."
 port.write(tdata)
 rcv = port.readline()
 if rcv:
  print(rcv)
  sys.exit("done")
