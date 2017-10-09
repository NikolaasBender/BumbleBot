# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
mode=GPIO.getmode()
GPIO.cleanup()

ForwardL = 26
BackwardL = 19
ForwardR = 13
BackwardR = 6
sleeptime = 1

GPIO.setup(ForwardL, GPIO.OUT)
GPIO.setup(BackwardL, GPIO.OUT)
GPIO.setup(ForwardR, GPIO.OUT)
GPIO.setup(BackwardR, GPIO.OUT)

FL = GPIO.PWM(26, 100)
BL = GPIO.PWM(19, 100)
FR = GPIO.PWM(13, 100)
BR = GPIO.PWM(6, 100)
FL.start(0)
BL.start(0)
FR.start(0)
BR.start(0)

t = 0.2

for dc in range(0, 101, 1):
	FL.ChangeDutyCycle(dc)
	FR.ChangeDutyCycle(dc)
	time.sleep(t)
for dc in range(100, -1, -1):
	FL.ChangeDutyCycle(dc)
	FR.ChangeDutyCycle(dc)
	time.sleep(t)
	
for dc in range(0, 101, 1):
	BL.ChangeDutyCycle(dc)
	BR.ChangeDutyCycle(dc)
	time.sleep(t)
for dc in range(100, -1, -1):
	BL.ChangeDutyCycle(dc)
	BR.ChangeDutyCycle(dc)
	time.sleep(t)

FL.stop()
BL.stop()
FR.stop()
BR.stop()

GPIO.cleanup()