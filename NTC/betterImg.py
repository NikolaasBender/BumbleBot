import cv2

camera = cv2.VideoCapture(0)

training_data = []

IMG_SIZE = 128

for i in range(0,10):
	return_val, image = camera.read()
	cv2.imwrite('ocv' + str(i) + '.png', image)
	new_array = cv2.resize(image, (IMG_SIZE, IMG_SIZE))  
	training_data.append(new_array)

del(camera)
