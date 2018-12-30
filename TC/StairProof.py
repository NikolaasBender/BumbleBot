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

#THESE ARE THE PIN OUTS FOR THE ULTRASOUND SENSOR
TRIG = 26
ECHO = 19

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


print "BEFORE FAR"

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

print "BEFORE STAIR CHECK"
#========================================
#THIS RETURNS THE DECISION ABOUT
#THERE BEING A STAIR
#========================================  
def stairCheck():
	tot = 0
	x = 0
	times = 0
	for x in range(0, 10): 
		dist = 0
		dist = far()
		if dist < 50:
			times += 1
			tot += dist
	atot = tot/times
	
#MAKES A DECISION OFF OF THE AVERAGE DISTANCE OF THE DISTANCE MEASUREMENTS
	if atot > 20:
		return True
	if atot <= 20:
		return False

print "BEFORE MAIN"		
#===========================================
#THE MEAT AND POTATOES
#===========================================
q = 0
while True:
	#print "FALSE"
	if stairCheck() == False:
		print "FORWARDS"
		time.sleep(0.1)
	#print "TRUE"
	if stairCheck() == True:
		print "STAIR! GO BACK!"
		time.sleep(0.1)

GPIO.cleanup()