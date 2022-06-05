import torch
import cv2
import os 
import code

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Images
imgs = []
for i in os.listdir('../test'):
    path = os.path.join('../test', i)
    imgs.append(cv2.imread(path))

# Inference
results = model(imgs)
code.interact(local=locals())
results.print()  # or .show(), .save()