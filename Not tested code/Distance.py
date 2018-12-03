import RPi.GPIO as GPIO


# #THESE ARE THE PIN OUTS FOR THE ULTRASOUND SENSOR
TRIG = 15
ECHO = 14

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

#THIS IS FOR DISTANCE SENSING
tot = 0
times = 0
x = 0

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