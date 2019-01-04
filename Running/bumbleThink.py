import cv2
import tensorflow as tf

CATEGORIES = ["halls", "stairs", "wallInFront", "wallOnLeft", "wallOnRight"]


def prepare(filepath):
    IMG_SIZE = 128 
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

testImgs = ["dangerTest.jpeg", "hallsTest.jpeg", "stairsTest.jpeg", "wfrontTest.jpeg", "wleftTest.jpeg", "wrightTest.jpeg"]

model = tf.keras.models.load_model("BumbleNet.model")

for test in testImgs:
	prediction = model.predict([prepare(test)])
	# will be a list in a list.
	print(prediction)  
	print(CATEGORIES[int(prediction[0][0])])