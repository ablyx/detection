Run docker container
```
cd /hdd/projs/detection

sudo docker run --ipc=host --gpus all -it -w /usr/src/detection -v "$(pwd)":/usr/src/detection -v /hdd/iphone2022:/hdd/iphone2022 yolov5:exif
```    

`cd src`  
get trip images
`python preprocess.py`
this will run preprocess to get trip images
`python detection.py`  

To build the docker image:
cd /hdd/projs/detection
docker build -f DOCKERFILE -t yolov5:exif .