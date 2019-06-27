import serial
from move_servo import wire

# THIS WORKS!!!!
# WOOHOO
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.write(b'H')
ser.write(b'L')
ser.write(b'H')
ser.write(b'L')
ser.close()

arduino = wire("ttyUSB0")


arduino.send()
