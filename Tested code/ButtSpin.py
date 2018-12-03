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

#PIN OUTS FOR THE MOTORS
ForwardL = 26
BackwardL = 19
ForwardR = 13
BackwardR = 6
sleeptime = 1
FrontL = 16
FrontM = 20
FrontR = 21

#WHEEL DIAMETER IN CM
diam = 9

GPIO.setup(ForwardL, GPIO.OUT)
GPIO.setup(BackwardL, GPIO.OUT)
GPIO.setup(ForwardR, GPIO.OUT)
GPIO.setup(BackwardR, GPIO.OUT)
GPIO.setup(FrontR, GPIO.IN)
GPIO.setup(FrontM, GPIO.IN)
GPIO.setup(FrontL, GPIO.IN)

#THIS IS THE PWM SETUP FOR THE MOTORS
FL = GPIO.PWM(ForwardL, 100)
BL = GPIO.PWM(BackwardL, 100)
FR = GPIO.PWM(ForwardR, 100)
BR = GPIO.PWM(BackwardR, 100)
FL.start(0)
BL.start(0)
FR.start(0)
BR.start(0)

# #THESE ARE THE PIN OUTS FOR THE ULTRASOUND SENSOR
# TRIG = 26
# ECHO = 19

# GPIO.setup(TRIG,GPIO.OUT)
# GPIO.setup(ECHO,GPIO.IN)

#THIS IS FOR DISTANCE SENSING
tot = 0
times = 0
x = 0

#THIS IS THE DUTY CYCLE FOR THE PWM CONTROL
dc = 0

#===================================
#RANDOM TURN RIGHT
#===================================
def turnR_R():
	dc = 50
	#LEFT FORWARD AND RIGHT BACKWARDS
	FL.ChangeDutyCycle(dc)
	BR.ChangeDutyCycle(dc)
	#SLEEP TO LET THE MOTOR CHOOCH
	time.sleep(random.uniform(1.0, 2.0))
	#TURN THE MOTORS OFF
	dc = 0
	FL.ChangeDutyCycle(dc)
	BR.ChangeDutyCycle(dc)

#=====================================
#RANDOM TURN LEFT
#=====================================
def turnL_R():
	#THIS TELLS THE MOTORS TO SPIN AT A SPECIFIC SPEED
	#THIS MAKES THEM RUN AT HALF SPEED
	dc = 50
	BL.ChangeDutyCycle(dc)
	FR.ChangeDutyCycle(dc)
	#THIS MAKES THEM SPIN FOR A SPECIFC AMOUNT OF TIME
	time.sleep(random.uniform(1.0, 2.0))
	#THIS TURNS THE MOTORS OFF\
	dc = 0
	BL.ChangeDutyCycle(dc)
	FR.ChangeDutyCycle(dc)

#========================================
#SPECIFIC TURN RIGHT
#TIM DETERMINES HOW LONG IT TURNS
#SPED IS THE SPEED IN PWM DUTY CYCLE PERCENTAGE
#========================================
def turnR_T(tim, sped):
	dc = sped
	#LEFT FORWARD AND RIGHT BACKWARDS
	FL.ChangeDutyCycle(dc)
	BR.ChangeDutyCycle(dc)
	#SLEEP TO LET THE MOTOR CHOOCH
	time.sleep(tim)
	#TURN THE MOTORS OFF
	dc = 0
	FL.ChangeDutyCycle(dc)
	BR.ChangeDutyCycle(dc)

	
#========================================
#SPECIFIC TURN LEFT
#TIM DETERMINES HOW LONG IT TURNS
#SPED IS THE SPEED IN PWM DUTY CYCLE PERCENTAGE
#========================================
def turnL_T(tim, sped):
	#THIS TELLS THE MOTORS TO SPIN AT A SPECIFIC SPEED
	#THIS MAKES THEM RUN AT HALF SPEED
	dc = sped
	BL.ChangeDutyCycle(dc)
	FR.ChangeDutyCycle(dc)
	#THIS MAKES THEM SPIN FOR A SPECIFC AMOUNT OF TIME
	time.sleep(tim)
	#THIS TURNS THE MOTORS OFF\
	dc = 0
	BL.ChangeDutyCycle(dc)
	FR.ChangeDutyCycle(dc)


#========================================
#THIS IS TO CHOOSE A NEW DIRECTION IF 
#THE FRONT BUTTON IS PUSHED
#========================================
def randomF():
	decision = random.randint(0,1)
	
	#LEFT TURN
	#TURNS RIGHT WHEEL FORWARDS AND LEFT WHEEL BACKWARDS
	if decision == 0:
		turnL_R()
	#RIGHT TURN
	if decision == 1:
		turnR_R()
	
#=====================================
#THIS IS TO CHOOSE A NEW DIRECTION 
#WHEN THE FRONT RIGHT BUTTON IS PUSHED
#======================================
	
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
	dist = 0
	x = 0
	tot = 0
	times = 0
	for x in range(0, 10): 
		dist = far()
		if dist < 50:
			tot += dist
			times += 1
	atot = tot/times
	print(atot)
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
	#RPM AT SPECIFIC DUTY CYCLE
	rpm = dc / 2
	#FIGURES OUT THE CIRCUMFRENCE OF THE WHEEl
	circ = diam * math.pi
	#SPEED IN CM/S
	speed = (rpm * circ) / 60
	#CM / (CM/S) = S
	endr = cm / speed
	
	return endr
		
#======================================================
#THIS IS WHERE ALL ALL OF IT GOES
#======================================================

while True:
	if FrontR == True:
		turnL_R
	if FrontL == True:
		turnR_R
	#if FrontM == True:




BR.stop()
BL.stop()
FL.stop()
FR.stop()

GPIO.cleanup()


		
