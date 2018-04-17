#Import the OpenCV and dlib libraries
import cv2
import numpy as np



#Initialize a face cascade using the frontal face haar cascade provided with
#the OpenCV library
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#The deisred output width and height
OUTPUT_SIZE_WIDTH = 775
OUTPUT_SIZE_HEIGHT = 600

def detectAndTrackLargestFace():
    #Open the first webcame device
    capture = cv2.VideoCapture(0)

    #Retrieve the latest image from the webcam
    while 1:
        rc,fullSizeBaseImage = capture.read()

        baseImage = cv2.resize( fullSizeBaseImage, ( 320, 240))

        resultImage = baseImage.copy()

        gray = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, 1.3, 5)

        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(baseImage, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = baseImage[y:y + h, x:x + w]

        cv2.imshow('img', baseImage)
        cv2.waitKey(2)




if __name__ == '__main__':
    detectAndTrackLargestFace()