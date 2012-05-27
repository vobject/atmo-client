import os
import sys
import time
import serial

def print_cmd(data):
  data_ord = [ord(x) for x in data]
  print "s:R%s.G%s.B%s - l:R%s.G%s.B%s - r:R%s.G%s.B%s - t:R%s.G%s.B%s - b:R%d.G%d.B%d" % (
           data_ord[ 4], data_ord[ 5], data_ord[ 6],
           data_ord[ 7], data_ord[ 8], data_ord[ 9],
           data_ord[10], data_ord[11], data_ord[12],
           data_ord[13], data_ord[14], data_ord[15],
           data_ord[16], data_ord[17], data_ord[18])

ser = serial.Serial(port="/dev/pts/5",
                    baudrate=38400,
                    parity=serial.PARITY_NONE,
                    bytesize=serial.EIGHTBITS,
                    stopbits=serial.STOPBITS_ONE)

if ser.isOpen():
  while True:
    try:
      data = ser.read(19)
      print_cmd(data)
#      time.sleep(1)
    except KeyboardInterrupt:
      print "stopped"
      ser.close()
      break

