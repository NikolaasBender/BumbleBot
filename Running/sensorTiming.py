from time import sleep,time
from bum3Support import *
from bum3Const import *
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import numpy as np

GPIO.setmode(GPIO.BCM)
#=============================================================================
#THIS GETS THE DISTANCE FROM THE ULTRASOUND SENSORS
#REPORTS IN METERS
#=============================================================================
#PINS SHOULD BE A LIST WHRE [TRIGGER, ECHO]
def far(pins):
	# This function measures a distance
  GPIO.output(pins[0], True)
  sleep(0.000001)
  GPIO.output(pins[0], False)
  start = time()

  while GPIO.input(pins[1])==0:
    start = time()

  stop = time()
  while GPIO.input(pins[1])==1:
    stop = time()

  elapsed = stop-start
  distance = (elapsed * 343)/2

  return distance

#=============================================================================
#THIS RETURNS BETTER DISTANCES
#... HOPEFULLY
#=============================================================================
def get_wall(pins):
	dists = []
	for i in range(0,10):
		dists.append(far(pins))
	dists.sort()
	tmp = 0
	mid = dists[5]
	cnt = 0
	for x in range(0,10):
		need = dists[x]
		if need <= mid * 1.5 and need >= mid * 0.5:
			tmp += need
			cnt += 1
	
	return tmp / cnt



tests = 1000


#THIS IS THE SENSOR SETUP FOR THE LEFT SENSOR
cSens = Sensor(11, 9)

ms = [7, 8]
GPIO.setup(ms[0], GPIO.OUT)
GPIO.setup(ms[1], GPIO.IN)

clooptim = []
mlooptim = []
mast = []

try:
	for x in range(1, tests):
		
		print("TESTING")

		#TEST FOR THE CLASS IMPLEMENTATION
		cdat = []
		cloop = time()
		throwAway0 = cSens.get_wall()
		clooptim.append(time() - cloop)




		#TEST FOR THE REGULAR METHOD IMPLEMENTATION
		mloop = time()
		hrowAway1 = get_wall(ms)
		mlooptim.append(time() - mloop)
		
		mast.append(x)

	plt.plot(clooptim, label = "cloop")
	plt.plot(mlooptim, label = "mloop")

	plt.savefig('fulldat.png')

	print((sum(clooptim) / 999) , " clooptim avg")
	print((sum(mlooptim) / 999) , " mlooptim avg")

except KeyboardInterrupt:
	print("Exiting")

finally:
	GPIO.cleanup()