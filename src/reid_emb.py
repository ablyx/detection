import os
import sys
from detection import get_people_bboxs
sys.path.insert(0, '/usr/src/detection/src/reid')
from encoder import OsNetEncoder
from detection import get_people_bboxs
from preprocess import get_trip_images, get_im_from_heif
import code
import numpy as np
import pickle

encoder = OsNetEncoder(
    input_width=704,
    input_height=480,
    weight_filepath="/usr/src/detection/models/osnet_ibn_ms_d_c.pth.tar",
    batch_size=32,
    num_classes=2022,
    patch_height=256,
    patch_width=128,
    norm_mean=[0.485, 0.456, 0.406],
    norm_std=[0.229, 0.224, 0.225],
    GPU=True)

def get_reid_emb():
    EMBS_PKL = "/usr/src/detection/save/reid_embs.pkl"
    if os.path.isfile(EMBS_PKL):
        with open(EMBS_PKL, 'rb') as f:
            reid_embs = pickle.load(f)
    else:
        fps = get_trip_images()
        bboxs = get_people_bboxs()
        ppl_crops = []
        count = 0
        for bbox in bboxs:
            idx = bbox[0].astype(int)
            x,y,w,h = bbox[1:5].astype(int)
            im = get_im_from_heif(fps[idx])
            #person_crop = im[y:y+h, x:x+w]
            person_crop = im.crop((x-w//2,y-h//2,x+w//2,y+h//2))
            #person_crop2 = im.crop((y,x,y+h,x+w))
            """ 
            if len(ppl_crops) < 10:
                pass
                #person_crop.save(f"../save/person_crop_test{count}.jpg")
                #person_crop2.save("../save/person_crop_test2.jpg")
            else:
                break
                #exit()
            """
            """
            if count == 10:
                break
            """
            count+=1

            #print(person_crop.size)
            #print(fps[idx])
            cw, ch = person_crop.size
            if cw == 0 or ch == 0:
                print(fps[idx], cw, ch)
            ppl_crops.append(person_crop)
        print("get_features")
        embs_lst = encoder.get_features(ppl_crops)
        embs = np.vstack(embs_lst)
        #idxs_col = bboxs[:,0][:count]
        idxs_col = bboxs[:,0]
        idxs_col_2d = np.expand_dims(idxs_col, 1)
        #code.interact(local=dict(globals(), **locals()))
        reid_embs = np.hstack([idxs_col_2d, embs]) 
        with open(EMBS_PKL, 'wb') as f:
            pickle.dump(reid_embs, f)
    return reid_embs

if __name__ == "__main__":
    get_reid_emb()