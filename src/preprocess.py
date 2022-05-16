import pyheif
import exiftool
import os
import code
from datetime import datetime

# want to get all heic files between 06/04/2022 and 24/04/2022 in /hdd/iphone
def get_trip_images():
    start_date = datetime.strptime("06/04/2022", "%d/%m/%Y")
    end_date = datetime.strptime("25/04/2022", "%d/%m/%Y")
    FOLDER = "/hdd/iphone2022"
    et = exiftool.ExifToolHelper()
    for f in os.listdir(FOLDER):
        if not f.endswith(".HEIC"):
            continue
        fp = os.path.join(FOLDER, f)
        metadata = et.get_metadata(fp)[0]
        curr_date = metadata["EXIF:DateTimeOriginal"]
        curr_dt = datetime.strptime(curr_date, '%Y:%m:%d %H:%M:%S')
        if curr_dt >= start_date and curr_dt < end_date:
            print(metadata['SourceFile'])        

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
