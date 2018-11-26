

#A FRESH START

from gpiozero import DistanceSensor
from gpiozero import Motor
from time import sleep
import random
import os
import multiprocessing as mp

#THIS IS TO ACTIVATE OR DEACTIVATE PRINT STATEMENTS
debugmode = 0

#THE SIZE OF THE WHEELS IN MM
ws = 90

#THE RPM OF THE MOTORS AT 100% POWER
rpm = 50

#HOW FAR SHOULD THE ROBOT MOVE BEFORE CHECKING FOR STAIRS IN MM
chkDst = 50

#STAIR SENSOR HEIGHT IN M
stairSens = 0.2

#SETTING UP CAMERA STUFF
piccount = 0



# SETUP MOTORS
Lmotor = Motor(forward=4, backward=14)
Rmotor = Motor(forward=4, backward=14)
FMsensor = DistanceSensor(23, 24)
Mbutton = Button(2)
Rbutton = Button(3)
Lbutton = Button(4)


#=============================================================================
#THIS CALCULATES THE TIME TO WAIT TO GO A CERTIAN DISTANCE
#=============================================================================
def disT(speed):
	#WE GET CIRCUMFRENCE
	c = 3.14*ws
	rps = speed * rmp / 60
	#c * r/s = mm/s HOW FAR IT MOVES EVERY SECOND
	#WE WANT TO CHECK EVERY Xcm
	#s*(c*r/s) = chkDst
	return chkDst / (c * rps)



def snap(count):
	os.system("fswebcam -r 1280x720  --no-banner /home/pi/images/$DATE.%d.jpg" %count)


#=============================================================================
#THIS IS THE MAIN LOOP
#=============================================================================
while True:

	#THIS MIGHT NOT BE NECESSARY
	#THIS CLEARS ANY INSTRUCTIONS TO THE MOTORS WAITING FOR NEW INSTRUCTIONS
	Lmotor.stop()
	Rmotor.stop()


	p = mp.Process(target = snap, args=(piccount,))
	p.start()
	piccount += 1


	#NO STAIR ALL IS GOOD
	if FMsensor.distance <= stairSens:

		#WE CAN USE 0-1 FOR SPEED
		speed = 1
		dist = disT(speed)

		#MIDDLE HARDWARE BUTTON
		if Mbutton == True:
			if debugmode == 1:
				print("MIDDLE BUTTON! BACK IT UP!")

			Lmotor.backward()
			Rmotor.backward()
			#GIVE 'ER MORE TURN BUD!
			sleep(dist+1)

		#RIGHT HARDWARE BUTTON
		if Rbutton == True:
			if debugmode == 1:
				print("RIGHT BUTTON PUSHED! GO LEFT!")

			Rmotor.stop()
			Lmotor.backward(speed)
			#GIVE 'ER MORE TURN BUD!
			sleep(dist+1)

		#LEFT HARDWARE BUTTON 
		if Lbutton == True:
			if debugmode == 1:
				print("LEFT BUTTON PUSHED! GO RIGHT")

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
	    
	    sleep(0.1)
	    
	    Lmotor.backward(speed)
	    Rmotor.backward(speed)

	    #RANDOMLY CHOOSE A NEW DIRECTION A GO FORWARD
		#WE'LL JUST START WITH TURNING 90deg TO RIGHT OR LEFT
		rl = random.getrandbits(1)

		#GO RIGHT
		if rl == 1:
			if debugmode == 1:
				print("GOING RIGHT!")
			Rmotor.backward(speed)
			Lmotor.stop()
			#LETS JUST TRY WAITING 2 SECS AND SEE HOW FAR IT TURNS 
			sleep(2)

		#GO LEFT
		if rl == 0:
			if debugmode == 1:
				print("GOING LEFT!")
			Lmotor.backward(speed)
			Rmotor.stop()
			#LETS JUST TRY WAITING 2 SECS AND SEE HOW FAR IT TURNS 
			sleep(2)