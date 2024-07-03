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

    # finding contours
    contours, hierachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    try:
        # finding contour with maximum area
        contour = max(contours, key=lambda x: cv2.contourArea(x))

        # creating bounding rectangle around the contour
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(crop_image, (x,y), (x+w,y+h), (0,0,225), 0)

        # finding convex hull
        hull = cv2.convexHull(contour)

        # drawing contour(green) and hull(blue)
        drawing = np.zeros(crop_image.shape, np.uint8)
        cv2.drawContours(drawing, [contour], -1, (0,255,0), 0)
        cv2.drawContours(drawing, [hull], -1, (0,0,255), 0)

        # Fi convexity defects
        hull = cv2.convexHull(contour, returnPoints=False)
        defects = cv2.convexityDefects(contour, hull)

        # using consine rule to find angle of the far point from the start and end point
        # i.e. the convex points (the finger tips) for all defects
        count_defects = 0

        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])
        
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

            # if angle >= 90 draw a circle at the far point
            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_image, far, 1, [0, 0, 255], -1)

            cv2.line(crop_image, start, end, [0, 255, 0], 2)

        # if more than 4 fingers are counted, press SPACE
        if count_defects >= 4:
                pyautogui.press('space')
                cv2.putText(frame, "JUMP", (115, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)

        #PLAY RACING GAMES (WASD)
        if count_defects == 1:
            pyautogui.press('w')
            cv2.putText(frame, "W", (115, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
        if count_defects == 2:
            pyautogui.press('s')
            cv2.putText(frame, "S", (115, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
        if count_defects == 3:
            pyautogui.press('aw')
            cv2.putText(frame, "aw", (115, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
        if count_defects == 4:
            pyautogui.press('dw')
            cv2.putText(frame, "dw", (115, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
        if count_defects == 5:
            pyautogui.press('s')
            cv2.putText(frame, "s", (115, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
    
    except:
        pass

    # showing required images
    cv2.imshow("Gesture", frame)

    # closing the camera if 'q' is pressed
    if cv2.waitKey(1) == ord('q'): break

capture.release()
cv2.destroyAllWindows()