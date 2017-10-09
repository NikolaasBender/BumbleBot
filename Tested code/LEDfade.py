import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

#channel 26 at 50hz
p = GPIO.PWM(26, 100)
p.start(0)
try:
	while 1:
		for dc in range(0, 101, 5):
		 p.ChangeDutyCycle(dc)
		 time.sleep(0.1)
		for dc in range(100, -1, -5):
		 p.ChangeDutyCycle(dc)
		 time.sleep(0.1)
except KeyboardInterrupt:
	pass
p.stop()
GPIO.cleanup()
