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



