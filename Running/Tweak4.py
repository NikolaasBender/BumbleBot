from gpiozero import DistanceSensor, Motor, Button
from time import sleep,time
import random
import os
import multiprocessing as mp
import RPi.GPIO as GPIO

#THIS IS FOR TWEAK THE 4 SENSORS ON BUMBLEBOT
FMsensor = DistanceSensor(echo = 20, trigger = 21)
Msens = DistanceSensor(echo = 8, trigger = 7)
Rsens = DistanceSensor(echo = 16, trigger = 12)
Lsens = DistanceSensor(echo = 11, trigger = 9)

#THE NUMBER OF TESTS
tot = 10000


#ANALYZE THE DATA FOR THE DELTA, MIN, MAX
def diff(lA):
	maximum = 0.001
	minimum = 1.0
	for i in range(0,tot):
		if float(lA[i]) > float(maximum):
			maximum = lA[i]
		if float(lA[i]) < float(minimum) and float(lA[i]) != 0.0:
			minimum = lA[i]

	return ((maximum - minimum), minimum, maximum)



#THIS COMES UP THE THE PERCENTAGE OF OF THE DATA THAT IS BAD
def bad(a):
	cnt = 0
	for i in range(0,tot):
		if a[i] == 0.0:
			cnt += 1
	return cnt / tot


#THIS COUNTS THE NUMBER OF ZEROS IN THE DATA
def countz(a):
	cnt = 0
	for i in range(0,tot):
		if a[i] == 0.0:
			cnt += 1
	return cnt

#WHERE WE STORE THE DATA
rvec = []
lvec = []
mvec = []
dvec = []

start = time()

for i in range(0,tot):
	rvec.append(Rsens.distance)


for i in range(0,tot):
	lvec.append(Lsens.distance)


for i in range(0,tot):
	mvec.append(Msens.distance)


for i in range(0,tot):
	dvec.append(FMsensor.distance)

end = time()

r = (diff(rvec), countz(rvec), bad(rvec))
l = (diff(lvec), countz(lvec), bad(lvec))
m = (diff(mvec), countz(mvec), bad(mvec))
d = (diff(dvec), countz(dvec), bad(dvec))


print("delta          num 0s           % bad data")
print(r)
print(l)
print(m)
print(d)

print("runtime: ", end - start)


print("=====================================================")
print("===================SECOND TEST=======================")
print("=====================================================")

#WHERE WE STORE THE DATA
rvec1 = []
lvec1 = []
mvec1 = []
dvec1 = []

start1 = time()

for i in range(0,tot):
	rvec1.append(Rsens.distance)
	lvec1.append(Lsens.distance)
	mvec1.append(Msens.distance)
	dvec1.append(FMsensor.distance)

end1 = time()

r1 = (diff(rvec1), countz(rvec1), bad(rvec1))
l1 = (diff(lvec1), countz(lvec1), bad(lvec1))
m1 = (diff(mvec1), countz(mvec1), bad(mvec1))
d1 = (diff(dvec1), countz(dvec1), bad(dvec1))


print("delta          num 0s           % bad data")
print(r1)
print(l1)
print(m1)
print(d1)

print("runtime: ", end1 - start1)


print("=====================================================")
print("====================THIRD TEST=======================")
print("=====================================================")

ls = [9, 11]
rs = [12, 16]
ms = [7, 8]
ds = [21, 20]

rvec2 = []
lvec2 = []
mvec2 = []
dvec2 = []

#========================================
#THIS GETS THE DISTANCE FROM THE ULTRASOUND SENSORS
#REPORTS IN METERS
#========================================
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


start2 = time()

for i in range(0,tot):
	rvec2.append(get_wall(rs))
	lvec2.append(get_wall(ls))
	mvec2.append(get_wall(ms))
	dvec2.append(get_wall(ds))

end2 = time()

r2 = (diff(rvec2), countz(rvec2), bad(rvec2))
l2 = (diff(lvec2), countz(lvec2), bad(lvec2))
m2 = (diff(mvec2), countz(mvec2), bad(mvec2))
d2 = (diff(dvec2), countz(dvec2), bad(dvec2))


print("delta          num 0s           % bad data")
print(r2)
print(l2)
print(m2)
print(d2)

print("runtime: ", end2 - start2)
