import pyheif
import exiftool
import os
import pickle
import code
from datetime import datetime
from PIL import Image

# want to get all heic files between 06/04/2022 and 24/04/2022 in /hdd/iphone
# this is speicfic to usa trip. Maybe I should just write a function and store the images in another folder for better sorting?
# then also refactor this to be more extensible to generic trip folders. 
def get_trip_images():
    # this part here is extremely non-generic for now. 
    # should refactor this. especially so because I will be reusing this in detection.py
    TRIP_IMGS_PKL = "/usr/src/detection/save/trip_imgs_fps.pkl" 
    if os.path.isfile(TRIP_IMGS_PKL):
        with open(TRIP_IMGS_PKL, "rb") as f:
            im_path_lst = pickle.load(f) 
    else:
        start_date = datetime.strptime("06/04/2022", "%d/%m/%Y")
        end_date = datetime.strptime("25/04/2022", "%d/%m/%Y")
        FOLDER = "/hdd/iphone2022"
        et = exiftool.ExifToolHelper()
        im_path_lst = []
        for f in os.listdir(FOLDER):
            if not f.endswith(".HEIC"):
                continue
            fp = os.path.join(FOLDER, f)
            metadata = et.get_metadata(fp)[0]
            curr_date = metadata["EXIF:DateTimeOriginal"]
            curr_dt = datetime.strptime(curr_date, '%Y:%m:%d %H:%M:%S')
            if curr_dt >= start_date and curr_dt < end_date:
                # print(metadata['SourceFile'])
                im_path_lst.append(fp)        
        with open(TRIP_IMGS_PKL, "wb") as f:
            pickle.dump(im_path_lst, f)
    return im_path_lst

def get_im_from_heif(fp):
    heif_file = pyheif.read(fp)
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    return image

def test_exif(files):
    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(files)
    for d in metadata:
        #code.interact(local=locals())
        print("{:20.20} {:20.20}".format(d["SourceFile"],
                                         d["EXIF:DateTimeOriginal"]))

def get_date_created(fpath):
    heif_file = pyheif.read(fpath)
    non_img_bytes = heif_file[1]
    
if __name__ == "__main__":
    folder = "/hdd/iphone2022"
    files = ["IMG_8888.HEIC", "IMG_8887.HEIC", "IMG_8149.HEIC"]
    files = list(map(lambda x:os.path.join(folder,x), files))
    test_exif(files)
    get_trip_images()
