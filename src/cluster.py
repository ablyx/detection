from cmath import atanh
import pickle
from sklearn.cluster import KMeans
from cfg import mslogger
import os 
from preprocess import get_trip_images
from detection import get_people_bboxs

def kmeans_cluster(embs,n):
    cluster_ids = KMeans(n_clusters=n).fit_predict(embs)
    return cluster_ids

def viz_clusters(c_ids, bbox_idxs, NUM_CLUSTERS):
    im_path_lst = get_trip_images()
    bboxs = get_people_bboxs()
    """
    for b in bbox_idxs:
        print(b.astype(int))
    """
    print(len(im_path_lst))
    cluster_root_folder = "../cluster_txt"
    lst_of_clusters = [[] for i in range(NUM_CLUSTERS)]
    for i, im_idx in enumerate(bbox_idxs):
        c_id = c_ids[i]
        #print(bboxs[bbox_idx], bbox_idx)
        #im_idx = bboxs[bbox_idx][0].astype(int)
        im_fp = im_path_lst[im_idx]
        lst_of_clusters[c_id].append(im_fp)
    print(lst_of_clusters)
    #exit()
    for c_id, lst in enumerate(lst_of_clusters):
        write_str = '\n'.join(lst)
        fp = os.path.join(cluster_root_folder, f'c{c_id}.txt')
        with open(fp, 'w') as f:
            f.write(write_str)
    return

if __name__ == "__main__":
    # reid_embs = np.hstack([idxs_col_2d, embs]) 

    EMBS_PKL = "/usr/src/detection/save/reid_embs.pkl"
    if not os.path.isfile(EMBS_PKL):
        mslogger.trace(f"{EMBS_PKL} file not found") 
        exit()

    NUM_CLUSTERS = 50
    with open(EMBS_PKL, 'rb') as f:
        reid_id_embs = pickle.load(f)
    reid_embs = reid_id_embs[:,1:]
    c = kmeans_cluster(reid_embs, NUM_CLUSTERS)    
    print(c.shape)
    viz_clusters(c, reid_id_embs[:, 0].astype(int), NUM_CLUSTERS)