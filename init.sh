-#!/bin/bash

set -e

## docker creation
#docker build  --network="host" -t caegomezji/fordat:latest .

## run container
docker run  -t --rm \
    --name  fordat  \
    --net="host" \
    -v "$PWD":/var/www \
    caegomezji/fordat:latest \
    /bin/bash  -l -c "./serve.sh"
