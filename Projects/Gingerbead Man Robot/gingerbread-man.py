

# Build an Edible Gingerbread Robot With the Raspberry Pi and Servos
'''
This is by far the tastiest project we've ever done!  In this project we show you how to build a Gingerbread robot using the Raspberry Pi and servos kit, and the Raspberry Pi Servo Controller.  The Gingerbread robot is equipped with a camera that checks for faces, and if it sees a face, it does a small dance!

We naturally had to take this a little further, and added facial recognition to the mix: the robot can detect a face using OpenCV and the Raspberry Pi Camera.
'''
# Some of this code is borrowed from: https://pythonprogramming.net/raspberry-pi-camera-opencv-face-detection-tutorial/

import io
import picamera
import cv2
import numpy
import time
import datetime
import pivotpi

try:
	pivotpi = pivotpi.PivotPi(0x40, 60)
except:
	print("PivotPi not found - quitting")
	exit(-1)


def check_for_face():

	#Create a memory stream so photos doesn't need to be saved in a file
	stream = io.BytesIO()

	#Get the picture (low resolution, so it should be quite fast)
	#Here you can also specify other parameters (e.g.:rotate the image)
	with picamera.PiCamera() as camera:
		camera.resolution = (320, 240)
		camera.capture(stream, format='jpeg')

	#Convert the picture into a numpy array
	buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

	#Now creates an OpenCV image
	image = cv2.imdecode(buff, 1)
	

	#Load a cascade file for detecting faces
	face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.1.0/data/haarcascades/haarcascade_frontalface_alt.xml')

	#Convert to grayscale
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	#Look for faces in the image using the loaded cascade file
	faces = face_cascade.detectMultiScale(gray, 1.1, 5)

	print "Found "+str(len(faces))+" face(s)"

	if len(faces) > 0:
		#Draw a rectangle around every found face
		for (x,y,w,h) in faces:
			cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)

		date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
		#Save the result image
		image_name = date_string+'.jpg'
		cv2.imwrite(image_name,image)

	return len(faces)

print('Merry Christmas, press Ctrl-C to quit...')

def pivot_arms():
	pivotpi.angle(0, 1)
	pivotpi.angle(1, 100)
	pivotpi.led(0, 0)
	time.sleep(1)
	
	pivotpi.angle(0, 100)
	pivotpi.angle(1, 1)
	pivotpi.led(100, 0)
	time.sleep(1)
	print("Arms!")

while True:
	# Check for a Face
	face = check_for_face()
	print(str(face))
	# If you Find a Face, Say Hello!
	if face > 0:
		pivot_arms()
		pivot_arms()
