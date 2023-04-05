import urllib.request
import cv2
import numpy as np
import mediapipe as mp
import requests
import pymongo
import threading

chat_ids=None


# client = pymongo.MongoClient("mongodb+srv://harshnishad:harshnishad@cluster0.llahgwx.mongodb.net/test")
# db2 = client["tele_id"]
# keys=db2["keys"]
# chat_ids = keys.find({},{"_id":0,"chat_id":1})







print(chat_ids)
def send_alert(chat_id):
    token = "6184416177:AAGzElvMve5KnyiCEh7l9b3Plh526ILkrL0"
    

    alert_msg="Alert! Someone is at your door."


    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
       "chat_id": chat_id,
       "text": alert_msg
    }
    resp = requests.get(url, params=params)

    # # Throw an exception if Telegram API fails
    # resp.raise_for_status()



def send_alert_all():
    for chat_id in chat_ids:
        send_alert(chat_id["chat_id"])

url = "http://192.168.184.236:8080/shot.jpg"

# Initialize Mediapipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

ESP_URL = "http://192.168.184.181/"
ULTRA_THRESHOLD = 40

def HandleRequest(request):
    requests.get(ESP_URL + request)

def getDistanceFromESP():
    response = requests.get(ESP_URL)
    return float(response.text.split(" ")[0].split("<")[0])


direction = "up"

HandleRequest("pose")
HandleRequest(direction)

print("Starting")

# Start capturing frames from the IP webcam
i = 1
while True:
    # Read image from the IP webcam
    img_resp = urllib.request.urlopen(url)
    img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    image = cv2.imdecode(img_arr, -1)
    image = cv2.resize(image, (640, 480))

    # Convert the image from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image with Mediapipe Pose model
    results = pose.process(image)

    # Draw the pose landmarks on the image
    if results.pose_landmarks is not None:
        print(f"person detected {i}")
        i+=1
        #send alert to all users
        #send_alert_all()
        continue
    # Display the image with the pose landmarks
    #qqcv2.imshow('Mediapipe Pose Detection', image)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #stop esp
        HandleRequest("stop")
        break
    if cv2.waitKey(5) & 0xFF == 27:
        HandleRequest("stop")

        break


# Release resources
#stop
HandleRequest("stop")
pose.close()
cv2.destroyAllWindows()
