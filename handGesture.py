import math
import cv2
import mediapipe as mp
import requests
import numpy as np
import urllib.request
import requests
import threading
import json

#mp drawing


import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
distanceMin = 9
distanceMax = 50
thresholdM = 0.25*(distanceMax - distanceMin)
thresholdT = 0.25
ESP_URL = "http://192.168.184.181/"
THRESHOLDC = 7
THRESHOLDD = 15
THRESHOLDM =25

url = "http://192.168.184.90:8080/shot.jpg"


def handle_motion(centerX, centerY, distance):
    if distance > distanceMax - thresholdM:
        print("move backward")
    elif distance < distanceMin + thresholdM:
        print("move forward")
    else:
        print("don't move")
    if centerX > 1-thresholdT:
        print("turn right")
    elif centerX < thresholdT:
        print("turn left")
    else:
        print("don't turn")


def handleRequest(direction):
    requests.get(ESP_URL + direction)



def handleGesture(hand_landmarks):
    if hand_landmarks is None:
        requests.get(ESP_URL + "stop")
        return
    else:
        indexTipX= hand_landmarks.landmark[8].x
        indexTipY= hand_landmarks.landmark[8].y

        ThumbTipX= hand_landmarks.landmark[4].x
        ThumbTipY= hand_landmarks.landmark[4].y

        middleTipX= hand_landmarks.landmark[12].x
        middleTipY= hand_landmarks.landmark[12].y

        distIndexThumb = math.sqrt((indexTipX - ThumbTipX)**2 + (indexTipY - ThumbTipY)**2) * 100
        distIndexMiddle = math.sqrt((indexTipX - middleTipX)**2 + (indexTipY - middleTipY)**2) * 100
        
        littleStartX = hand_landmarks.landmark[17].x
        littleStartY = hand_landmarks.landmark[17].y

        ringStartX = hand_landmarks.landmark[13].x
        ringStartY = hand_landmarks.landmark[13].y

        ringTipX = hand_landmarks.landmark[16].x
        ringTipY = hand_landmarks.landmark[16].y


        palmX = hand_landmarks.landmark[0].x
        palmY = hand_landmarks.landmark[0].y

        distRingTipPalm = math.sqrt((ringTipX - palmX)**2 + (ringTipY - palmY)**2) * 100
        littleTipX = hand_landmarks.landmark[20].x
        littleTipY = hand_landmarks.landmark[20].y

        distLittle = math.sqrt((littleStartX - littleTipX)**2 + (littleStartY - littleTipY)**2) * 100

        # print(distIndexThumb, distIndexMiddle, distRingTipPalm)
        isIndexMiddle = distIndexMiddle > THRESHOLDC
        if distRingTipPalm > THRESHOLDM :
            threading.Thread(target=handleRequest, args=("rt",)).start()
            print("turn")

        elif not isIndexMiddle and distIndexThumb > THRESHOLDD:
            threading.Thread(target=handleRequest, args=("up",)).start()
            print("up")
        elif isIndexMiddle and distIndexThumb > THRESHOLDD:
            threading.Thread(target=handleRequest, args=("down",)).start()
            print("down")
        else:
            threading.Thread(target=handleRequest, args=("stop",)).start()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

while True:
    hand_landmarks = None
    img_resp = urllib.request.urlopen(url)
    img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    image = cv2.imdecode(img_arr, -1)

    # Resize the image to 640x480
    image = cv2.resize(image, (640, 480))

    try:
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        hand_landmarks = results.multi_hand_landmarks[0]
        # #draw the line between index and thumb
        cv2.line(image, (int(hand_landmarks.landmark[4].x*640), int(hand_landmarks.landmark[4].y*480)), (int(hand_landmarks.landmark[8].x*640), int(hand_landmarks.landmark[8].y*480)), (255, 0, 0), 2)

        # #draw the line between index and middle
        cv2.line(image, (int(hand_landmarks.landmark[8].x*640), int(hand_landmarks.landmark[8].y*480)), (int(hand_landmarks.landmark[12].x*640), int(hand_landmarks.landmark[12].y*480)), (0, 255, 0), 2)

    #     #draw the line between palm and ringTip
        
        cv2.line(image, (int(hand_landmarks.landmark[0].x*640), int(hand_landmarks.landmark[0].y*480)), (int(hand_landmarks.landmark[16].x*640), int(hand_landmarks.landmark[16].y*480)), (0, 0, 255), 2)

        # x1 = hand_landmarks.landmark[5].x
        # y1 = hand_landmarks.landmark[5].y
        # x2 = hand_landmarks.landmark[0].x
        # y2 = hand_landmarks.landmark[0].y
        # cv2.line(image, (int(x1*640), int(y1*480)), (int(x2*640), int(y2*480)), (255, 0, 0), 2)
        # cv2.circle(image, (int(x1*640), int(y1*480)), 5, (0, 0, 255), -1)
        # cv2.circle(image, (int(x2*640), int(y2*480)), 5, (0, 0, 255), -1)
        # cv2.putText(image, str(math.sqrt((x1-x2)**2 + (y1-y2)**2)), (int(x1*640), int(y1*480)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        # centerX = (x1+x2)/2
        # centerY = (y1+y2)/2
        # distance = math.sqrt((x1-x2)**2 + (y1-y2)**2) * 100
        # if 0 <= distance <= 100:
            # cv2.circle(image, (int(centerX*640), int(centerY*480)), 5, (0, 255, 0), -1)
            # handle_motion(centerX, centerY, distance)
        #draw the hand landmarks
        #mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)


    except:
        print("No hand detected")
        pass
    handleGesture(hand_landmarks)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

hands.close()
cv2.destroyAllWindows()

