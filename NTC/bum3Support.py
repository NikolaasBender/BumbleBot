from time import sleep,time
import datetime
import random
import os
import multiprocessing as mp
import RPi.GPIO as GPIO
from bum3Const import *


GPIO.setmode(GPIO.BCM)



#=============================================================================
#THIS CALCULATES THE TIME TO WAIT TO GO A CERTIAN DISTANCE
#=============================================================================
def disT(speed):
	#WE GET CIRCUMFRENCE
	c = 3.14*ws
	rps = speed * rpm / 60
	#c * r/s = mm/s HOW FAR IT MOVES EVERY SECOND
	#WE WANT TO CHECK EVERY Xcm
	#s*(c*r/s) = chkDst
	return chkDst / (c * rps)


#=============================================================================
#THIS TAKES A PHOTO
#=============================================================================
def snap():
	while True:
		file = datetime.datetime.now().strftime('%Y-%m-%d_%I-%M-%S%p') + ".jpeg"
		pic = "streamer -q -s 128x128 -o images/" + file
		#bw = "bw.cpp " + file
		cmd = pic #+ "&&" + bw
		os.system(cmd)
		# move = "sshpass -p PASSWORD scp " + file + " you@computer:/Pictures/data/"
		# os.system(move)

		sleep(2)





def ranNewDir(l, r):
	#RANDOMLY CHOOSE A NEW DIRECTION A GO FORWARD
	#WE'LL JUST START WITH TURNING 90deg TO RIGHT OR LEFT
	rl = random.getrandbits(1)

	speed = 0.3
	#THIS SHOULD BE TWEAKED IN THE FUTURE USING SOME MATH
	#BUT FOR NOW GUESSING WORKS FINE
	turny = 0.5

	#GO RIGHT
	if rl == 1:
		if debugmode == 1:
			print("GOING RIGHT!")
		r.forward(speed)
		#LETS JUST TRY WAITING 2 SECS AND SEE HOW FAR IT TURNS 
		sleep(turny)

	#GO LEFT
	if rl == 0:
		if debugmode == 1:
			print("GOING LEFT!")
		l.forward(speed)
		#LETS JUST TRY WAITING 2 SECS AND SEE HOW FAR IT TURNS 
		sleep(turny)



class Motor:
	"""docstring for Motor"""
	def __init__(self, pin1, pin2):
		self.pin1 = pin1
		self.pin2 = pin2
		GPIO.setup(self.pin1, GPIO.OUT)
		GPIO.setup(self.pin2, GPIO.OUT)
		p1 = GPIO.PWM(self.pin1, 100)
		p2 = GPIO.PWM(self.pin2, 100)
		self.p1 = p1
		self.p2 = p2
		self.p1.start(0)
		self.p2.start(0)
	
	def forward(self, speed):
		self.p2.ChangeDutyCycle(0)
		self.p1.ChangeDutyCycle(speed * 100)

	def backward(self, speed):
		self.p1.ChangeDutyCycle(0)
		self.p2.ChangeDutyCycle(speed * 100)

	def stop(self):
		self.p1.ChangeDutyCycle(0)
		self.p2.ChangeDutyCycle(0)




class Sensor:
	"""docstring for Sensor"""
	def __init__(self, echo, trig):
		self.echo = echo
		self.trig = trig
		GPIO.setup(self.trig, GPIO.OUT)
		GPIO.setup(self.echo, GPIO.IN)
		

	#=============================================================================
	#THIS GETS THE DISTANCE FROM THE ULTRASOUND SENSORS
	#REPORTS IN METERS
	#=============================================================================
	#PINS SHOULD BE A LIST WHRE [TRIGGER, ECHO]
	def far(self):
		# This function measures a distance
		GPIO.output(self.trig, True)
		
		sleep(0.000001)
		GPIO.output(self.trig, False)
		start = time()

		while GPIO.input(self.echo)==0:
			start = time()

		stop = time()
		while GPIO.input(self.echo)==1:
			stop = time()

		elapsed = stop-start
		distance = (elapsed * 343)/2

		return distance

	#=============================================================================
	#THIS RETURNS BETTER DISTANCES
	#=============================================================================
	def get_wall(self):
		dists = []
		for i in range(0,10):
			dists.append(self.far())
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