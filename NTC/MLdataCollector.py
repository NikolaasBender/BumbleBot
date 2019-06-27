from bum3Support import *
import cv2
from controller import *
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os
import numpy as np

Lmotor = Motor(26, 19)
Rmotor = Motor(13, 6)

file_name = 'training_data.npy'

#last = []

def rC(ctrl):
	#global last
	speed = 0.5

	if ctrl[2] == 1:
		Lmotor.forward(speed)
		Rmotor.stop()
	if ctrl[0] == 1:
		Rmotor.forward(speed)
		Lmotor.stop()
	if ctrl[1] == 1:
		Rmotor.forward(speed)
		Lmotor.forward(speed)
	if ctrl[3] == 1:
		Rmotor.backward(speed)
		Lmotor.backward(speed)

	if ctrl[1] == 1 and ctrl[0] == 1:
		Rmotor.forward(speed*0.6)
		Lmotor.forward(speed)
	if ctrl[1] == 1 and ctrl[2] == 1:
		Rmotor.forward(speed)
		Lmotor.forward(speed*0.6)

	if ctrl == [0, 0, 0, 0]:
		Rmotor.stop()
		Lmotor.stop()
	
	return 


#USEFUL FOR RESIZING THE IMAGE
IMG_SIZE = 128

#INSTANTIATE TRAINING DATA
training_data = []

#CAMERA SETUP FOR WEBCAM
#cam = cv2.VideoCapture(0)
#PICAM SETUP
camera = PiCamera()
rawCapture = PiRGBArray(camera)

#SETUP THE GAMEPAD
jstest = gpControl()

#SAVE LIMIT
SL = 500

try:
		
	if os.path.isfile(file_name):
		print('File exists, loading previous data!')
		training_data = list(np.load(file_name))
	else:
		print('File does not exist, starting fresh!')
		training_data = []

	while 1:

		#THIS GETS THE BUTTONS BEING PRESSED ON THE CONTROLLER
		tmp = jstest.process_events()

		#THIS TAKES THE DATA FOR LEARNING
		if type(tmp) != None:
			try:

				#GET AN IMAGE IF USING WEBCAM
				#ret, frame = cam.read()
				#GET IMAGE IF USING PICAM
				camera.capture(rawCap, format="bgr")
				frame = rawCapture.array

				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY )

				#RESIZE AND NORMALIZE THE IMAGE
				new_array = cv2.resize(gray, (IMG_SIZE, IMG_SIZE))  

				#ADD THE IMAGE DATA AND GAMEPAD DATA TO 
				training_data.append([new_array, tmp]) 

				if len(training_data) % 500 == 0:
					print(len(training_data))
					np.save(file_name,training_data)

					

			except Exception as e:  # in the interest in keeping the output clean...
				pass
			#THIS USED THE BUTTON PRESSES TO CONTROL THE ROBOT
			rC(tmp)
except KeyboardInterrupt:
	print("Exiting")

finally:
	np.save(file_name,training_data)
	exit()
