

#A FRESH START
# https://gpiozero.readthedocs.io/en/stable/recipes.html
#HOPEFULLY THIS WILL SPEED UP DEVELOPMENT A LITTLE BIT AND CLEAN SOME STUFF UP

from gpiozero import DistanceSensor
from gpiozero import Motor
from time import sleep

#WE WILL USE THIS TO CALCULATE THE WAIT TIME BASED ON SPEED AND STUFF
debugmode = 0

#THE SIZE OF THE WHEELS IN MM
ws = 90

#THE RPM OF THE MOTORS AT 100% POWER
rpm = 50

#HOW FAR SHOULD THE ROBOT MOVE BEFORE CHECKING FOR STAIRS IN MM
chkDst = 50

#STAIR SENSOR HEIGHT IN M
stairSens = 0.2


# SETUP MOTORS
Lmotor = Motor(forward=4, backward=14)
Rmotor = Motor(forward=4, backward=14)
FMsensor = DistanceSensor(23, 24)
Mbutton = Button(2)

def disT(speed):
	#WE GET CIRCUMFRENCE
	c = 3.14*ws
	rps = speed * rmp / 60
	#c * r/s = mm/s HOW FAR IT MOVES EVERY SECOND
	#WE WANT TO CHECK EVERY Xcm
	#s*(c*r/s) = chkDst
	return chkDst / (c * rps)




#IF THE DISTANCE SENSOR SAYS THERE IS STILL FLOOR UNDER THE ROBOT
while True:

	if FMsensor.distance <= stairSens:
		
		#WE CAN USE 0-1 FOR SPEED
		speed = 1
		
		if debugmode == 1:
			print("GOING FORWARD")
	    
	    Lmotor.forward(speed)
	    Rmotor.forward(speed)
	    sleep(disT(speed))
	
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

	