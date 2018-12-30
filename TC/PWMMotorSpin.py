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

FL = GPIO.PWM(ForwardL, 100)
BL = GPIO.PWM(BackwardL, 100)
FR = GPIO.PWM(ForwardR, 100)
BR = GPIO.PWM(BackwardR, 100)
FL.start(0)
BL.start(0)
FR.start(0)
BR.start(0)

t = 3
dc = 100

#SPIN FORWARDS
FL.ChangeDutyCycle(dc)
FR.ChangeDutyCycle(dc)
time.sleep(t)
	
#STOP ALL
FL.ChangeDutyCycle(0)
FR.ChangeDutyCycle(0)
BL.ChangeDutyCycle(0)
BR.ChangeDutyCycle(0)

#SPIN BACK
BL.ChangeDutyCycle(dc)
BR.ChangeDutyCycle(dc)
time.sleep(t)

FL.stop()
BL.stop()
FR.stop()
BR.stop()

GPIO.cleanup()