# This script detects the glass and hat at some confidence level
import cv2
import numpy as np
import os
import time
import datetime

# Load YOLO Algorithm
net = cv2.dnn.readNet("yolov3_custom_final.weights", "yolov3_custom.cfg")
# To load all objects that have to be detected
classes = []
with open("obj1.names", "r") as f:
    read = f.readlines()
for i in range(len(read)):
    classes.append(read[i].strip("\n"))

# Defining layer names
layer_names = net.getLayerNames()
output_layers = []
for i in net.getUnconnectedOutLayers():
    output_layers.append(layer_names[i - 1])

# Loading the Image
img = cv2.imread("picture.jpg")
height, width, channels = img.shape
# Extracting features to detect objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
# Inverting blue with red
# bgr->rgb
# We need to pass the img_blob to the algorithm
net.setInput(blob)
outs = net.forward(output_layers)
# print(outs)
# Displaying information on the screen
class_ids = []
confidences = []
boxes = []
for output in outs:
    for detection in output:
        # Detecting confidence in 3 steps
        scores = detection[5:]  # 1
        class_id = np.argmax(scores)  # 2
        confidence = scores[class_id]  # 3
        if confidence > 0.4:  # Means if the object is detected
            print(class_id)
            print(confidence)
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            # Drawing a rectangle
            x = int(center_x - w / 2)  # top left value
            y = int(center_y - h / 2)  # top left value
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)
        # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

# Removing Double Boxes
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = classes[class_ids[i]]  # name of the objects
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, label, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

scale_percent = 50  # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)

# resize image
resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
cv2.imshow("Output", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
