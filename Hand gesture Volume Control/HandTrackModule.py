import time
import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.7, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLMS,self.mpHands.HAND_CONNECTIONS)
        return img   

    def findPosition(self,img,handNo = 0, draw = True):
        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id,lm in enumerate(myHand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id,cx,cy])

                if draw:
                    cv2.circle(img,(cx,cy),10,(255,0,255))

                # if id == 4:
                #     cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)    
        return lmList              
                 

def main():
    cap = cv2.VideoCapture(0)
    ptime, ctime = 0, 0
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img,draw=False)
        if len(lmList) != 0:
            print(lmList[4])
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        txt = f'FPS : {int(fps)}'

        cv2.putText(img, txt, (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
