#!/bin/bash

## docker creation
docker build  --network="host" -t caegomezji/fordat:latest .

## run container
docker run  -it --rm \
    --name  fordat  \
    --net="host"  \
    -v "$PWD":/var/www \
    caegomezji/fordat:latest \
    /bin/bash  # 