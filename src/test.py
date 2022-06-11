import torch
import cv2
import os 
import code
import pickle

def test_yolo_model():
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

def test_reid_embs():
    with open("../save/reid_embs.pkl", 'rb') as f:
        embs = pickle.load(f)
    print(type(embs))
    print(embs.shape)
    print(embs[:,0])

if __name__ == "__main__":
    test_reid_embs()