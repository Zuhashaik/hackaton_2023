#!git clone https://github.com/ultralytics/yolov5
import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
from gtts import gTTS
import os
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

language = 'en'

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
detected_objects=[""]

while cap.isOpened():
    ret, frame = cap.read()

    # Make detections
    results = model(frame)

    cv2.imshow('Object Detection', np.squeeze(results.render()))
    for i, det in enumerate(results.pred):
        for *xyxy, conf, cls in det:
            score = conf.item()
            if (model.names[int(cls)]) in detected_objects:
                pass
            else:
                if score>0.50:

                 mytext="I detect a "+detected_objects[-1]
                 detected_objects.append(model.names[int(cls)])
                 mytext=str(mytext)
                 print(mytext)

                 myobj = gTTS(text=mytext, lang=language, slow=True)

                 myobj.save("welcome.mp3")

                 # Playing the converted file
                 os.system("open welcome.mp3")

            if len(detected_objects)>3:
                detected_objects.pop(0)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
