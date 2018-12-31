from gpiozero import DistanceSensor, Motor, Button
from time import sleep,time
import random
import os
import multiprocessing as mp

FMsensor = DistanceSensor(echo = 20, trigger = 21)
Msens = DistanceSensor(echo = 8, trigger = 7)
Rsens = DistanceSensor(echo = 16, trigger = 12)
Lsens = DistanceSensor(echo = 11, trigger = 9)

#min distance is 1ft 30cm

high = 0.6
low = 0.1
ok = 0.1337
limit = 5
tot = 10000
waiter = 0.005

def Ls():
	avg = 0.0
	cnt = 0.0
	for x in range(0,10):
		tmp = Lsens.distance
		if cnt == limit:
			return avg / x
		if tmp < high and tmp > low:
			avg += tmp
		else:
			cnt += 1
			x -= 1
	return avg/10


def Rs():
	avg = 0.0
	cnt = 0.0
	for x in range(0,10):
		tmp = Rsens.distance
		if cnt == limit:
			return avg / x
		if tmp < high and tmp > low:
			avg += tmp
		else:
			cnt += 1
			x -= 1
	return avg/10


def Ms():
	avg = 0.0
	cnt = 0.0
	for x in range(0,10):
		tmp = Msens.distance
		if cnt == limit:
			return avg / x
		if tmp < high and tmp > low:
			avg += tmp
		else:
			cnt += 1
			x -= 1
	return avg/10


def Ds():
	avg = 0.0
	cnt = 0.0
	for x in range(0,10):
		tmp = FMsensor.distance
		if cnt == limit:
			return avg / x
		if tmp < high and tmp > low:
			avg += tmp
		else:
			cnt += 1
			x -= 1
	return avg/10



def diff(lA):
	maximum = 0.001
	minimum = 1.0
	for i in range(0,tot):
		if float(lA[i]) > float(maximum):
			maximum = lA[i]
		if float(lA[i]) < float(minimum) and float(lA[i]) != 0.0:
			minimum = lA[i]

	return ((maximum - minimum), minimum, maximum)


def countz(a):
	cnt = 0
	for i in range(0,tot):
		if a[i] == 0.0:
			cnt += 1
	return cnt


def bad(a):
	cnt = 0
	for i in range(0,tot):
		if a[i] == 0.0:
			cnt += 1
	return cnt / tot

rvec = []
lvec = []
mvec = []
dvec = []

start = time()
for i in range(0,tot):
	rvec.append(Rs())

sleep(waiter)

for i in range(0,tot):
	lvec.append(Ls())
	
sleep(waiter)
for i in range(0,tot):
	mvec.append(Ms())

sleep(0.05)
for i in range(0,tot):
	dvec.append(Ds())

end = time()


print("rs delta: ", diff(rvec))
print("ls delta: ", diff(lvec))
print("ms delta: ", diff(mvec))
print("ds delta: ", diff(dvec))

print("rs 0s: ", countz(rvec))
print("ls 0s: ", countz(lvec))
print("ms 0s: ", countz(mvec))
print("ds 0s: ", countz(dvec))

print("rs bad data: ", bad(rvec))
print("ls bad data: ", bad(lvec))
print("ms bad data: ", bad(mvec))
print("ds bad data: ", bad(dvec))

print("test time: ", end - start)