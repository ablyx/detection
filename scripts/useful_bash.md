
find -iname *.heic | wc -l
source det_env/bin/activate

cd /hdd/projs/detection
sudo docker run --ipc=host -it -v "$(pwd)":/usr/src/detection ultralytics/yolov5:latest
