from ultralytics import YOLO
import cvzone
import cv2  
import math  
import pygame  
      
# Initialize pygame for playing sound 
pygame.init()
 
# Load the sound file (replace 'alarm_sound.wav' with the path to your sound file)
alarm_sound = pygame.mixer.Sound('alarm_sound.wav')

# Running real-time from webcam
cap = cv2.VideoCapture('fire4.mp4')
model = YOLO('fire.pt')

# Reading the classes
classnames = ['fire']

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    result = model(frame, stream=True)

    # Getting bbox, confidence, and class names information to work with
    for info in result:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence * 100)
            Class = int(box.cls[0])
            if confidence > 50:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', [x1 + 8, y1 + 100],
                                   scale=1.5, thickness=2)

                # Play the alarm sound when fire is detected
                alarm_sound.play()

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
