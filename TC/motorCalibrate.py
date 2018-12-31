#CALIBRATION SCRIPT
from gpiozero import DistanceSensor, Motor, Button
from time import sleep,time
import RPi.GPIO as GPIO


Lmotor = Motor(forward=26, backward=19)
Rmotor = Motor(forward=13, backward=6)

speed = 0.5

print("right motor forward")
Rmotor.forward(speed)
sleep(5)


print("right motor backward")
Rmotor.backward(speed)
sleep(5)

Rmotor.stop()

print("left motor forward")
Lmotor.forward(speed)
sleep(5)


print("left motor backward")
Lmotor.backward(speed)
sleep(5)

Lmotor.stop()

GPIO.cleanup()