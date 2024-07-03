import numpy as np
import cv2
import math

# python module for controlling mouse and keyboard without needing user
import pyautogui

# opening camera and setting up the rectangle

# opening camera
capture = cv2.VideoCapture(0)

# while camera can seee
while capture.isOpened():

    # getting frames from the camera
    ret, frame = capture.read()

    # analyzing hand from the frame
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 0)
    crop_image = frame[100:300, 100:300]

    # blurring image to smooth out edges
    blur = cv2.GaussianBlur(crop_image, (3, 3), 0)

    # changing color from BGR(Blue, Green, Red) to HSV(Hue, Saturation, Value)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)



