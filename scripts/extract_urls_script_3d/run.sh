#!/bin/bash

docker run -it \
--net=host \
-e INPUT_PATH="/home/shayavr/Documents/3d-large-record.json" \
-e OUTPUT_PATH =""\
-v /tmp/urls_data:/urls/test_data \
extract-url-script:latest /bin/bash
