import torch
import cv2
import os 
import code
import pickle
from detection import get_people_bboxs
from preprocess import get_trip_images, get_im_from_heif

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

def test_detection_results():
    fps = get_trip_images()
    bboxs = get_people_bboxs()
    ppl_crops = []
    count = 0
    for bbox in bboxs:
        idx = bbox[0].astype(int)
        x,y,w,h = bbox[1:5].astype(int)
        im = get_im_from_heif(fps[idx])
        person_crop = im.crop((x-w//2,y-h//2,x+w//2,y+h//2))

        if len(ppl_crops) < 800:
            person_crop.save(f"../test_det/person_crop_test{count}.jpg")
        count += 1

if __name__ == "__main__":
    #test_reid_embs()
    test_detection_results()