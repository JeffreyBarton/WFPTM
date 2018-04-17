# USAGE
# python detect_faces_video.py --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel

# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import serial
import numpy as np
arduino = serial.Serial('COM4',115200,timeout=.1)

MAX = 180
min = MAX - 180
max = MAX - 0


def setServo(channel,pos):
    if pos >= max:
        pos = max
    elif pos < min:
        pos = min
    command = "Sending\n".encode() + str(channel).encode() + ",".encode() + str(round(int(pos))).encode() + "\n".encode()
    #print(command)
    done = False
    while not done:
        arduino.write(command)
        data = arduino.readline()
        #print(data)
        if data:
            a = data.decode("utf-8").split(',')
            if int(a[0]) ==  channel and abs(int(a[1])-pos) < 2:
                done = True
                #print("Success")

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

modelFile = 'res10_300x300_ssd_iter_140000.caffemodel'
protoFile = 'deploy.prototxt.txt'


# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(protoFile, modelFile)

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

Fh = 72.4
Fv = 44.7

RHorLeft = 20
RHorRight = 130
RVertBot = 110
RVertTop = 0

LHorLeft = 0
LHorRight = 100
LVertBot = 0
LVertTop = 180

posRightHor = 80

out = cv2.VideoWriter('HW7.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20.0, (int(400),int( 300)))

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	h_true,w_true = frame.shape[0:2]

 
	# grab the frame dimensions and convert it to a blob
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
		(300, 300), (104.0, 177.0, 123.0))
 
	# pass the blob through the network and obtain the detections and
	# predictions
	net.setInput(blob)
	detections = net.forward()

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with the
		# prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence < args["confidence"]:
			continue

		# compute the (x, y)-coordinates of the bounding box for the
		# object
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")

		[X,Y] = [(startX+endX)/2,(startY+endY)/2]

		RHorPos = X / w_true * (RHorRight - RHorLeft) + RHorLeft
		RVerPos = Y / h_true * (RVertBot - RVertTop)
		LHorPos = (X / w_true * (LHorRight - LHorLeft) + LHorLeft)
		LVerPos = LVertTop - (Y / h_true * (LVertTop - LVertBot))
		print(LHorPos)
		if abs(posRightHor-RHorPos) > 3:
		 	setServo(1, RHorPos)
		 	setServo(0, RVerPos)
		 	setServo(14, LHorPos)
		 	setServo(15, LVerPos)
			#time.sleep(20)

		area = (endX-startX)*(endY-startY)


 
		# draw the bounding box of the face along with the associated
		# probability
		text = "{:.2f}%".format(confidence * 100)
		y = startY - 10 if startY - 10 > 10 else startY + 10
		cv2.rectangle(frame, (startX, startY), (endX, endY),
			(0, 0, 255), 2)
		cv2.putText(frame, text, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

	# show the output frame
	out.write(frame)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(250) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
out.release()
cv2.destroyAllWindows()
vs.stop()