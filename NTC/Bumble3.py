
#The road to skynet
	#1/5/19 rev: Morty || Modern morty is updating the proof of concept Bumble2. It
	#still does all of the same stuff but its just an updated form thats cleaner and better


from time import sleep,time
from bum3Support import *
from bum3Const import *
import multiprocessing as mp


ls = Sensor(11, 9)
rs = Sensor(16, 12)
ms = Sensor(8, 7)
ds = Sensor(20,21)

rm = Motor(13, 6)
lm = Motor(26, 19)


#=============================================================================
#THIS IS THE MAIN LOOP
#=============================================================================
try:
	#THIS JUST TAKES PHOTOS EVERY 2 SECONDS AND SAVES THEM
	#IT RUNS INDEPENDENTLY OF EVERYTHING ELSE
	# p = mp.Process(target = snap)
	# p.start()
	# cturn = 0
	while True:

		#NO STAIR ALL IS GOOD
		depth = ds.get_wall()

		if debugmode == 1:
				print("DEPTH:", depth)

		#==========================================
		#THERE IS NO STAIR
		#==========================================
		if  depth <= stairSens:

			#WE CAN USE 0-1 FOR SPEED
			speed = 0.3
			extraTurn = 0.5
			dist = disT(speed)

			md = ms.get_wall()
			ld = ls.get_wall()
			rd = rs.get_wall()


			if debugmode == 1:
				print(ld, md, rd)

			cturn = 0

			#MIDDLE HARDWARE BUTTON
			if md <= wall:
				if debugmode == 1:
					print("MIDDLE BUTTON! BACK IT UP!")

				#p.start()
				rm.backward(speed)
				lm.backward(speed)
				#GIVE 'ER MORE TURN BUD!
				sleep(dist + 2)
				ranNewDir()


			#LEFT SIDE IS CLOSER TO A WALL
			if ld < rd and ld <= wall and rd <= wall:
				if debugmode == 1:
					print("LEFT BUTTON PUSHED! GO RIGHT")

				#p.start()
				lm.stop()
				rm.backward(speed)
				#GIVE 'ER MORE TURN BUD!
				sleep(dist + extraTurn)
				cturn = 1




			#RIGHT SIDE IS CLOSER TO A WALL
			if rd < ld and ld <= wall and rd <= wall:
				if debugmode == 1:
					print("RIGHT BUTTON PUSHED! GO LEFT!")

				#p.start()
				rm.stop()
				lm.backward(speed)
				#GIVE 'ER MORE TURN BUD!
				sleep(dist + extraTurn)
				cturn = 1




			#WALL DISTANCES ARE EQUAL
			if rd <= ld * 1.1 and rd >= ld * 0.9 and ld <= wall and rd <= wall:
				if debugmode == 1:
					print("EQUAL DISTANCES, CHOSING RANDOM NEW DIRECTION")

				rm.backward(speed)
				lm.backward(speed)
				sleep(dist + 3)
				ranNewDir()


			#RIGHT HARDWARE BUTTON
			if rd <= wall and cturn == 0: 
				if debugmode == 1:
					print("RIGHT BUTTON PUSHED! GO LEFT!")

				#p.start()
				lm.backward(speed)
				#GIVE 'ER MORE TURN BUD!
				sleep(dist + extraTurn)



			#LEFT HARDWARE BUTTON 
			if ld <= wall and cturn == 0:
				if debugmode == 1:
					print("LEFT BUTTON PUSHED! GO RIGHT")

				#p.start()
				rm.backward(speed)
				#GIVE 'ER MORE TURN BUD!
				sleep(dist + extraTurn)



			
			if debugmode == 1:
				print("GOING FORWARD")
		    
		    #GO FORWARD!!!
			rm.forward(speed)
			lm.forward(speed)
			sleep(dist)
		
		#==========================================
		#FOUND A STAIR
		#==========================================
		else:
			#BACKUP SPEED
			speed = 0.5

			if debugmode == 1:
				print("WE FOUND A STAIR! MAYDAY!!")
			
			#WE WANT TO STOP THE MOTORS AND PROBABLY BACKUP
			rm.stop()
			lm.stop()
		    
			# p.start()

			sleep(0.1)
		    
			rm.backward(speed)
			lm.backward(speed)

			sleep(1)

			#RANDOMLY CHOOSE A NEW DIRECTION A GO FORWARD
			#WE'LL JUST START WITH TURNING 90deg TO RIGHT OR LEFT
			ranNewDir(lm, rm)

except KeyboardInterrupt:
	print("Exiting")


finally:
	GPIO.cleanup()
	#p.terminate()
	exit()