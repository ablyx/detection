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

To build image for macos
docker build -f DOCKERFILE --build-arg BUILD_ENV=macos -t macos:base .

At home, instead of building it like yolov5:exif, this should work
docker build -f DOCKERFILE --build-arg BUILD_ENV=home -t macos:base .
