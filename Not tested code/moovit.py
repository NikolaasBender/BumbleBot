#MOOVIT METHOD
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

#PIN OUTS FOR THE MOTORS
def setup(fl, bl, fr, br, dm):
	#WHEEL DIAMETER IN CM
	diam = dm

	GPIO.setup(fl, GPIO.OUT)
	GPIO.setup(bl, GPIO.OUT)
	GPIO.setup(fr, GPIO.OUT)
	GPIO.setup(br, GPIO.OUT)

	#THIS IS THE PWM SETUP FOR THE MOTORS
	FL = GPIO.PWM(fl, 100)
	BL = GPIO.PWM(bl, 100)
	FR = GPIO.PWM(fr, 100)
	BR = GPIO.PWM(br, 100)
	FL.start(0)
	BL.start(0)
	FR.start(0)
	BR.start(0)


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
#THIS PURELY MOVES FORWARD
#IT ONLY MOVES FORWARDS 5cm AT A TIME
#======================================
def goFor():
	#STOPS THE MOTORS FROM SPINNING FORWARD
	dc = 0;
	BL.ChangeDutyCycle(dc)
	BR.ChangeDutyCycle(dc)

	#MAKES THEM SPIN BACKWARDS
	dc = 50
	FL.ChangeDutyCycle(dc)
	FR.ChangeDutyCycle(dc)
	time.sleep(movit(5, dc))


#=====================================
#THIS PURELY MOVES BACKWARD
#IT ONLY MOVES FORWARDS 20cm AT A TIME
#======================================
def goBak():
	#STOPS THE MOTORS FROM SPINNING FORWARD
	dc = 0;
	FL.ChangeDutyCycle(dc)
	FR.ChangeDutyCycle(dc)

	#MAKES THEM SPIN BACKWARDS
	dc = 50
	BL.ChangeDutyCycle(dc)
	BR.ChangeDutyCycle(dc)
	time.sleep(movit(20, dc))

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