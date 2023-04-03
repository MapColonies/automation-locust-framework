#!/bin/bash

docker run -it \
--net=host \
-e INPUT_PATH="/urls/csv_data/shay_example.json" \
-v /tmp/urls_data:/urls/test_data \
extract-url-script:latest /bin/bash
