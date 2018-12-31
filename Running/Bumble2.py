
#The road to skynet
	#12/24/18 rev: TIM || Runs away too much and doesn't want to go forward 

	#12/29/18(1am est) rev: PAUL || sensor issues should be fixed form TIM but 
	#right motor doesn't want to spin and left motor spins backwards with motor
	#controller getting really hot. No issues with motor calibration, even weirder

	#12/31/18 rev: GARRY || Garry goes! Bumble mini moves consistently and finds
	#its way with relative ease. Full bumblebot will need more sensors to make sure
	#its doesn't back over a stair or turn over a stair. The robot eats so 
	#much power too, I'm happy I have this giant lithium battery in the works. 

#from gpiozero import Motor, Button
from time import sleep,time
import random
import os
import multiprocessing as mp
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

#THIS IS TO ACTIVATE OR DEACTIVATE PRINT STATEMENTS
debugmode = 1

#THE SIZE OF THE WHEELS IN MM
ws = 64

#THE RPM OF THE MOTORS AT 100% POWER
rpm = 500

#HOW FAR SHOULD THE ROBOT MOVE BEFORE CHECKING FOR STAIRS IN MM
chkDst = 10

#STAIR SENSOR HEIGHT IN M
#THIS IS 6in IN M
stairSens = 0.152

#THIS IS THE WALL THRESH HOLD DISTANCE IN M
wall = 0.3

#SETTING UP CAMERA STUFF
piccount = 0


#THIS IS A DIAGRAM OF THE PINOUTS
# https://gpiozero.readthedocs.io/en/stable/_images/pin_layout.svg
#SETUP MOTORS
# Lmotor = Motor(forward=26, backward=19)
# Rmotor = Motor(forward=13, backward=6)




#MOTOR SETUP
# [FORWARD, BACKWARD]
lm = [26, 19]
rm = [13, 6]


GPIO.setup(lm[0], GPIO.OUT)
GPIO.setup(lm[1], GPIO.OUT)
GPIO.setup(rm[0], GPIO.OUT)
GPIO.setup(rm[1], GPIO.OUT)

#THIS IS THE PWM SETUP FOR THE MOTORS
FL = GPIO.PWM(lm[0], 100)
BL = GPIO.PWM(lm[1], 100)
FR = GPIO.PWM(rm[0], 100)
BR = GPIO.PWM(rm[1], 100)
FL.start(0)
BL.start(0)
FR.start(0)
BR.start(0)




#SENSOR SETUP
ls = [9, 11]
rs = [12, 16]
ms = [7, 8]
ds = [21, 20]


GPIO.setup(ls[0], GPIO.OUT)
GPIO.setup(ls[1], GPIO.IN)
GPIO.setup(rs[0], GPIO.OUT)
GPIO.setup(rs[1], GPIO.IN)
GPIO.setup(ms[0], GPIO.OUT)
GPIO.setup(ms[1], GPIO.IN)
GPIO.setup(ds[0], GPIO.OUT)
GPIO.setup(ds[1], GPIO.IN)






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
	# cmd = "streamer -f jpeg -o /home/pi/images/$DATE. " + string(time()) + ".jpeg"
	# os.system(cmd)
	return
	
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





#THIS STOPS ALL THE MOTORS SO THAT NOTHING CATCHES ON FIRE
def clear():
	FL.ChangeDutyCycle(0)
	BL.ChangeDutyCycle(0)
	FR.ChangeDutyCycle(0)
	BR.ChangeDutyCycle(0)




#DUTYCYCLE IS A VALUE BETWEEN 0 AND 1 
#AND THE DIRECTION IS 1 OR 0 FORWARD/BACKWARD
def Lspin(dutyCycle, direction):
	clear()
	if direction == 1:
		FL.ChangeDutyCycle(dutyCycle * 100)
	if direction == 0:
		BL.ChangeDutyCycle(dutyCycle * 100)





#DUTYCYCLE IS A VALUE BETWEEN 0 AND 1 
#AND THE DIRECTION IS 1 OR 0 FORWARD/BACKWARD
def Rspin(dutyCycle, direction):
	clear()
	if direction == 1:
		FR.ChangeDutyCycle(dutyCycle * 100)
	if direction == 0:
		BR.ChangeDutyCycle(dutyCycle * 100)


def Bspin(dutyCycle, direction):
	clear()
	if direction == 1:
		FR.ChangeDutyCycle(dutyCycle * 100)
		FL.ChangeDutyCycle(dutyCycle * 100)
	if direction == 0:
		BR.ChangeDutyCycle(dutyCycle * 100)
		BL.ChangeDutyCycle(dutyCycle * 100)



def ranNewDir():
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
		Rspin(speed, 1)
		#LETS JUST TRY WAITING 2 SECS AND SEE HOW FAR IT TURNS 
		sleep(turny)

	#GO LEFT
	if rl == 0:
		if debugmode == 1:
			print("GOING LEFT!")
		Lspin(speed, 0)
		#LETS JUST TRY WAITING 2 SECS AND SEE HOW FAR IT TURNS 
		sleep(turny)


#=============================================================================
#THIS IS THE MAIN LOOP
#=============================================================================
try:
	while True:


		p = mp.Process(target = snap)
		p.start()
		


		#NO STAIR ALL IS GOOD
		depth = get_wall(ds)

		if debugmode == 1:
				print("DEPTH:", depth)
		
		if  depth <= stairSens:

			#WE CAN USE 0-1 FOR SPEED
			speed = 0.3
			extraTurn = 0.5
			dist = disT(speed)

			md = get_wall(ms)
			ld = get_wall(ls)
			rd = get_wall(rs)

			if debugmode == 1:
				print(ld, md, rd)

			#MIDDLE HARDWARE BUTTON
			if md <= wall:
				if debugmode == 1:
					print("MIDDLE BUTTON! BACK IT UP!")

				#p.start()
				Bspin(speed, 0)
				#GIVE 'ER MORE TURN BUD!
				sleep(dist + extraTurn)
				ranNewDir()


			#LEFT SIDE IS CLOSER TO A WALL
			if ld < rd and ld <= wall and rd <= wall:
				if debugmode == 1:
					print("LEFT BUTTON PUSHED! GO RIGHT")

				#p.start()
				Rspin(speed, 0)
				#GIVE 'ER MORE TURN BUD!
				sleep(dist + extraTurn)




			#RIGHT SIDE IS CLOSER TO A WALL
			if rd < ld and ld <= wall and rd <= wall:
				if debugmode == 1:
					print("RIGHT BUTTON PUSHED! GO LEFT!")

				#p.start()
				Lspin(speed, 0)
				#GIVE 'ER MORE TURN BUD!
				sleep(dist + extraTurn)




			#WALL DISTANCES ARE EQUAL
			if rd == ld and ld <= wall and rd <= wall:
				if debugmode == 1:
					print("EQUAL DISTANCES, CHOSING RANDOM NEW DIRECTION")

				Bspin(dist, 0)
				ranNewDir()


			#RIGHT HARDWARE BUTTON
			if rd <= wall:
				if debugmode == 1:
					print("RIGHT BUTTON PUSHED! GO LEFT!")

				#p.start()
				Lspin(speed, 0)
				#GIVE 'ER MORE TURN BUD!
				sleep(dist + extraTurn)



			#LEFT HARDWARE BUTTON 
			if ld <= wall:
				if debugmode == 1:
					print("LEFT BUTTON PUSHED! GO RIGHT")

				#p.start()
				Rspin(speed, 0)
				#GIVE 'ER MORE TURN BUD!
				sleep(dist + extraTurn)



			
			if debugmode == 1:
				print("GOING FORWARD")
		    
		    #GO FORWARD!!!
			Bspin(speed, 1)
			sleep(dist)
		

		#GO BAKCWARDS
		else:
			#BACKUP SPEED
			speed = 0.5

			if debugmode == 1:
				print("WE FOUND A STAIR! MAYDAY!!")
			
			#WE WANT TO STOP THE MOTORS AND PROBABLY BACKUP
			clear()
		    
			# p.start()

			sleep(0.1)
		    
			Bspin(speed, 0)

			sleep(1)

			#RANDOMLY CHOOSE A NEW DIRECTION A GO FORWARD
			#WE'LL JUST START WITH TURNING 90deg TO RIGHT OR LEFT
			ranNewDir()

except KeyboardInterrupt:
	print("Exiting")

except:
	print("SOMETHING HAPPENED... EXITING")

finally:
	GPIO.cleanup()