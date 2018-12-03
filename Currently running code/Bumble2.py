

#A FRESH START

from gpiozero import DistanceSensor, Motor, Button
from time import sleep,time
import random
import os
import multiprocessing as mp


#THIS IS TO ACTIVATE OR DEACTIVATE PRINT STATEMENTS
debugmode = 1

#THE SIZE OF THE WHEELS IN MM
ws = 64

#THE RPM OF THE MOTORS AT 100% POWER
rpm = 500

#HOW FAR SHOULD THE ROBOT MOVE BEFORE CHECKING FOR STAIRS IN MM
chkDst = 10

#STAIR SENSOR HEIGHT IN M
#YOU NEED TO CHANGE THIS AND GET THE SENSOR TO WORK BETTER
stairSens = 0.2

#THIS IS THE WALL THRESH HOLD DISTANCE IN M
wall = 0.3

#SETTING UP CAMERA STUFF
piccount = 0


#THIS IS A DIAGRAM OF THE PINOUTS
# https://gpiozero.readthedocs.io/en/stable/_images/pin_layout.svg
#SETUP MOTORS
Lmotor = Motor(forward=27, backward=17)
Rmotor = Motor(forward=10, backward=22)
FMsensor = DistanceSensor(echo = 15, trigger = 14)
Msens = DistanceSensor(echo = 13, trigger = 21)
Rsens = DistanceSensor(echo = 26, trigger = 16)
Lsens = DistanceSensor(echo = 19, trigger = 20)

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



def snap():
	os.system("fswebcam -r 1280x720  --no-banner /home/pi/images/$DATE.%d.jpg" %time())
	

#=============================================================================
#THIS IS THE MAIN LOOP
#=============================================================================
while True:

	#THIS MIGHT NOT BE NECESSARY
	#THIS CLEARS ANY INSTRUCTIONS TO THE MOTORS WAITING FOR NEW INSTRUCTIONS
	Lmotor.stop()
	Rmotor.stop()


	# p = mp.Process(target = snap)
	# p.start()
	


	#NO STAIR ALL IS GOOD
	depth = FMsensor.distance

	if debugmode == 1:
			print("DEPTH: %d", depth)
	
	if  depth <= stairSens:

		#WE CAN USE 0-1 FOR SPEED
		speed = 0.25
		dist = disT(speed)

		#MIDDLE HARDWARE BUTTON
		if Msens.distance <= wall:
			if debugmode == 1:
				print("MIDDLE BUTTON! BACK IT UP!")

			#p.start()
			Lmotor.backward()
			Rmotor.backward()
			#GIVE 'ER MORE TURN BUD!
			sleep(dist+1)

		#RIGHT HARDWARE BUTTON
		if Rsens.distance <= wall:
			if debugmode == 1:
				print("RIGHT BUTTON PUSHED! GO LEFT!")

			#p.start()
			Rmotor.stop()
			Lmotor.backward(speed)
			#GIVE 'ER MORE TURN BUD!
			sleep(dist+1)

		#LEFT HARDWARE BUTTON 
		if Lsens.distance <= wall:
			if debugmode == 1:
				print("LEFT BUTTON PUSHED! GO RIGHT")

			#p.start()
			Lmotor.stop()
			Rmotor.backward(speed)
			#GIVE 'ER MORE TURN BUD!
			sleep(dist+1)
		
		if debugmode == 1:
			print("GOING FORWARD")
	    
	    #GO FORWARD!!!
		Lmotor.forward(speed)
		Rmotor.forward(speed)
		sleep(dist)
	
	else:
		#BACKUP SPEED
		speed = 1

		if debugmode == 1:
			print("WE FOUND A STAIR! MAYDAY!!")
		
		#WE WANT TO STOP THE MOTORS AND PROBABLY BACKUP
		Lmotor.stop()
		Rmotor.stop()
	    
		# p.start()

		sleep(0.1)
	    
		Lmotor.backward(speed)
		Rmotor.backward(speed)

		sleep(2)

		#RANDOMLY CHOOSE A NEW DIRECTION A GO FORWARD
		#WE'LL JUST START WITH TURNING 90deg TO RIGHT OR LEFT
		# rl = random.getrandbits(1)

		# #GO RIGHT
		# if rl == 1:
		# 	if debugmode == 1:
		# 		print("GOING RIGHT!")
		# 	Rmotor.backward(speed)
		# 	Lmotor.stop()
		# 	#LETS JUST TRY WAITING 2 SECS AND SEE HOW FAR IT TURNS 
		# 	sleep(2)

		# #GO LEFT
		# if rl == 0:
		# 	if debugmode == 1:
		# 		print("GOING LEFT!")
		# 	Lmotor.backward(speed)
		# 	Rmotor.stop()
		# 	#LETS JUST TRY WAITING 2 SECS AND SEE HOW FAR IT TURNS 
		# 	sleep(2)