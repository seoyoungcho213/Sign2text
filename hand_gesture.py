import numpy as np
import cv2
import math

# python module for controlling mouse and keyboard without needing user
import pyautogui

# OPENING THE CAMERA AND SETTING UP THE RECTANGLE

# opening camera
capture = cv2.VideoCapture(0)

# while camera can seee
while capture.isOpened():

    # getting frames from the camera
    ret, frame = capture.read()

    # analyzing hand from the frame
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 0)
    crop_image = frame[100:300, 100:300]

    # PREPROCESSING THE VISUAL DATA

    # blurring image to smooth out edges
    blur = cv2.GaussianBlur(crop_image, (3, 3), 0)

    # changing color from BGR(Blue, Green, Red) to HSV(Hue, Saturation, Value)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # further changing colors to black and white
    # so that all hand pixels are white and rest is black
    mask2 = cv2.inRange(hsv, np.array([2, 0, 0]), np.array([20, 255, 255]))

    # setting up kernal for morphological transformations
    kernel = np.ones((5, 5))

    # using it to filter out the background noise
    dilation = cv2.dilate(mask2, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=1)

    # applying Gaussian Blur and Threshold
    filtered = cv2.GaussianBlur(erosion, (3, 3), 0)
    ret, thresh = cv2.threshold(filtered, 127, 255, 0)

