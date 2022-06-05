import pickle
import os
from re import I
import numpy as np
import torch
from preprocess import get_trip_images, get_im_from_heif
import time
import logging
import code
from cfg import mslogger



def is_people_present(im):
    res = model(im)
    #code.interact(local=locals())
    if USE_GPU:
        res_np = res.xywh[0].cpu().numpy()
    else:
        res_np = res.xywh[0].numpy()
    # xywh,confidence,class
    return 0 in res_np[:, 5]

def get_people_bbox(im):
    res = model(im)
    #code.interact(local=locals())
    if USE_GPU:
        res_np = res.xywh[0].cpu().numpy()
    else:
        res_np = res.xywh[0].numpy()
    # xywh,confidence,class
    return res_np[res_np[:, 5]==0]


def get_people_bboxs():
    PPL_BBOXS_PKL = "/usr/src/detection/save/ppl_bboxs_fps.pkl"
    if os.path.isfile(PPL_BBOXS_PKL):
        with open(PPL_BBOXS_PKL, "rb") as f:
            ppl_bboxs = pickle.load(f) 
    else:
        start_time = time.time()
        im_path_lst = get_trip_images()
        end_time = time.time()
        time_taken = end_time-start_time
        mslogger.trace(f"get_trip_images time taken: {time_taken}") 
        people_im_path_lst = []
        #im_path_lst = ["/hdd/iphone2022/IMG_8131 2.HEIC", ]
        # idx,x,y,w,h,conf,cls
        res = np.array([]).reshape(0,7)
        for idx, im_path in enumerate(im_path_lst):
            # get PIL byte data from heif file
            im = get_im_from_heif(im_path)
            try:
                bboxs = get_people_bbox(im)
                #code.interact(local=dict(globals(), **locals())) 
                #if not bboxs and bboxs.shape[0] != 0:
                cols = bboxs.shape[0]
                if cols != 0:
                    idx_col = np.ones((cols, 1)) * idx
                    idx_bboxs = np.hstack([idx_col, bboxs])
                    res = np.vstack([res,idx_bboxs])
            except Exception as e:
                print(e)
                print("get_people_bbox", im_path)
                code.interact(local=dict(globals(), **locals())) 
        with open(PPL_BBOXS_PKL, "wb") as f:
            pickle.dump(res, f)
        ppl_bboxs = res
    return ppl_bboxs  

# dont really need this function if function above gets bboxs.
def get_people_images():
    PPL_IMGS_PKL = "/usr/src/detection/save/ppl_imgs_fps.pkl"
    if os.path.isfile(PPL_IMGS_PKL):
        with open(PPL_IMGS_PKL, "rb") as f:
            people_im_path_lst = pickle.load(f) 
    else:
        start_time = time.time()
        im_path_lst = get_trip_images()
        end_time = time.time()
        time_taken = end_time-start_time
        mslogger.trace(f"get_trip_images time taken: {time_taken}") 
        people_im_path_lst = []
        #im_path_lst = ["/hdd/iphone2022/IMG_8131 2.HEIC", ]
        for im_path in im_path_lst:
            # get PIL byte data from heif file
            im = get_im_from_heif(im_path)
            try:
                if is_people_present(im):
                    people_im_path_lst.append(im_path)
            except:
                print("is_people_present err", im_path)
        with open(PPL_IMGS_PKL, "wb") as f:
            pickle.dump(people_im_path_lst, f)
    return people_im_path_lst                            

#test = "IMG_9131 2.HEIC"

if __name__ == "__main__":
    USE_GPU = True 
    #model = torch.load('yolov5s.pt')
    if USE_GPU:
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s').cuda()
    else:
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s').cpu()

    mslogger.setLevel(logging.TRACE)
    start_time = time.time()
    #print(get_people_images()[:5])
    bboxs = get_people_bboxs()
    mslogger.trace(f"bboxs shape: {bboxs.shape}") 
    print(bboxs[:5])
    end_time = time.time()
    time_taken = end_time-start_time
    mslogger.trace(f"time taken: {time_taken}") 