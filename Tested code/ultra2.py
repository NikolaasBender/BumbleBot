#=====================================
#THIS IS IS ALL SETUP
#=====================================
# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

def far():
	# This function measures a distance
  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)
  start = time.time()

  while GPIO.input(ECHO)==0:
    start = time.time()

  while GPIO.input(ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * 34300)/2

  return distance
	

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

tot = 0
times = 0
x = 0

for x in range(0, 100):
	#print "TEST", x 
	dist = far()
	x -= 1
	if dist < 20:
		tot += dist
		times += 1
atot = tot/times


print "Distance:",atot,"cm"

GPIO.cleanup()