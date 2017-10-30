#=====================================
#THIS IS IS ALL SETUP
#=====================================
# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
mode=GPIO.getmode()
GPIO.cleanup()

TRIG = 26
ECHO = 19

print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, 0)
print "Waiting For Sensor To Settle"
time.sleep(0.1)

GPIO.output(TRIG, 1)
time.sleep(0.00001)
GPIO.output(TRIG, 0)

while GPIO.input(ECHO)==0:
  start = time.time()

while GPIO.input(ECHO)==1:
  end = time.time()
  
duration = end - start

distance = duration * 17000

distance = round(distance, 2)

print "Distance:",distance,"cm"

GPIO.cleanup()