#RESOURCES
#https://raspberrypi.stackexchange.com/questions/28428/how-to-control-an-l298-dual-h-bridge-motor-controller-with-gpio
#http://www.instructables.com/id/Raspberry-PI-L298N-Dual-H-Bridge-DC-Motor/
#ALL OF THIS CODE WAS LIFTED FROM THE INSTRUCTABLES SITE
#THIS CODE DOESNT USE PWM CONTROL
#THIS CODE DOES NOT HAVE ANY SPEED CONTROL

# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
mode=GPIO.getmode()
print " mode ="+str(mode)
GPIO.cleanup()

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24

Forward=26
Backward=19
sleeptime=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(Forward, GPIO.OUT)
GPIO.setup(Backward, GPIO.OUT)

#==========================
#X IS FORHOW LONG YOU WANT 
#IT TO SPIN FULL FORWARDS OR BACWARDS
#==========================
def forward(x):
    GPIO.output(Forward, GPIO.HIGH)
    print "forwarding running  motor "
    time.sleep(x)
    GPIO.output(Forward, GPIO.LOW)

def reverse(x):
    GPIO.output(Backward, GPIO.HIGH)
    print "backwarding running motor"
    time.sleep(x)
    GPIO.output(Backward, GPIO.LOW)

print "forward motor "
forward(5)
print "reverse motor"
reverse(5)

print "Stopping motor"
GPIO.cleanup()