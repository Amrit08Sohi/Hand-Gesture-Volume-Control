import cv2
import mediapipe as mp
import time
import numpy as np
from math import hypot
import HandTrackModule as htm

# To get the volume Control of computer
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)
minVol = volRange[0]
maxVol = volRange[1]

cap = cv2.VideoCapture(0)
# for track frame rate
ptime = 0 
# Object of hand detector
detector = htm.HandDetector()
vol = 0
# At volbar = 400 volume is at 0 level
volBar = 400
# Calculating volume Percentage
volPer = 0
while True:
    # To get the camera access to read the image
    success, img = cap.read()
    # Method to detect the hands 
    detector.findHands(img)
    # This list contains landmark values of hand and palm with its position at x and y axis
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # To get the thumb tip position at x(1) and y(2) axis 
        x1, y1 = lmList[4][1], lmList[4][2]
        # To get the index finger tip position at x(1) and y(2) axis 
        x2, y2 = lmList[8][1], lmList[8][2]
        # To get the center point between the distance of thumb tip and index finger tip
        cx, cy = (x1+x2)//2, (y1+y2)//2

        # Drawing a circle at thumb tip to visualize
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        # Drawing a circle at index finger tip to visualize
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        # draw a line that connects thumb tip and index finger tip
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        # Drawing a circle at center point btween thumb tip and index finger tip to visualize center point
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        # calculate the length between thumb tip and index finger tip
        # so that we can set or update  the volume according to length 
        length = hypot(x2-x1,y2-y1)
        # print(length)

        # Hand Range : 30 - 250
        # Vol Range :  -65 - 0
        # Here we use interpolation to plot the hand range and vol range
        # So that volume can automatically update according to hand range
        vol = np.interp(length,[30,250],[minVol,maxVol])

        # Here we set the volume visualizer height according to hand range
        # 400 is minimum means volume is at 0 level 
        # 150 is maximum means volume is at full level 
        volBar = np.interp(length,[30,250],[400,150])
        # Calculate volume percentage accoding to hand range
        volPer = np.interp(length,[30,250],[0,100])
        # print(int(length),vol)
        # this below line of code actually change the volume of system 
        volume.SetMasterVolumeLevel(vol, None)

        if length < 30 :
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    # This below code is used for volume visualizer
    cv2.rectangle(img,(50,150),(85,400),(255,0,0),2 )
    cv2.rectangle(img,(50,int(volBar)),(85,400),(255,0,0),cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}%', (40, 450),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)    
 
    # This below code is used to calculate the FPS
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    # Print the FPS on cmaera screen
    cv2.putText(img, f'Fps : {int(fps)}', (20, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # To open the camera 
    cv2.imshow("img", img)
    cv2.waitKey(1)
