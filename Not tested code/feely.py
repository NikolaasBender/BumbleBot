#FEELY

#=====================================
#THIS IS IS ALL SETUP
#=====================================
# Import required libraries
import sys
import time
import RPi.GPIO as GPIO
import math

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
mode=GPIO.getmode()
GPIO.cleanup()

#THIS IS FOR DISTANCE SENSING
tot = 0
times = 0
x = 0

#THIS IS THE DUTY CYCLE FOR THE PWM CONTROL
dc = 0

def setup(frl, frm, frr, e, t, dm):
	#WHEEL DIAMETER IN CM
	diam = dm

	GPIO.setup(frl, GPIO.IN)
	GPIO.setup(frm, GPIO.IN)
	GPIO.setup(frr, GPIO.IN)

	#THESE ARE THE PIN OUTS FOR THE ULTRASOUND SENSOR
	TRIG = t
	ECHO = e

	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)

#========================================
#THIS CHECKS FOR STAIRS USING
#THE ULTRA SOUND SENSOR
#========================================
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



#========================================
#THIS RETURNS THE DECISION ABOUT
#THERE BEING A STAIR
#========================================  
def stairCheck():
	for x in range(0, 100): 
		dist = far()
		x -= 1
		if dist < 50:
			tot += dist
			times += 1
	atot = tot/times
	
#MAKES A DECISION OFF OF THE AVERAGE DISTANCE OF THE DISTANCE MEASUREMENTS
	if atot > 20:
		return True
	if atot <= 20:
		return False



#===========================================
#THIS IS THE DISTANCE CONVERTER
#SO THAT WE CAN MOVE SPECIFIC DISTANCES
#CM IS THE DISTANCE WE WANT TO MOVE IN CM
#RETURNS A VLAUE IN SEC FOR THE WAIT FUNCTION
#===========================================
def movit(cm, dc):
	speed = dc * 0.5
	circ = diam * math.pi
	return 60/(speed * circ)