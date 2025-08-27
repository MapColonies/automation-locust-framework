#!/bin/bash

docker run -it \
--user $(id -u):$(id -g) \
-e output_file="/opt/attribute_value_mapping.json" \
-e TYPE_NAME="buildings" \
--net=host \
-e URL="https://geoserver-2-27-vector-dev.apps.j1lk3njp.eastus.aroapp.io/geoserver/core/wfs" \
-v /home/shayavr/Desktop/scripts_vols/:/opt/  \
vector-attribute-generator:v1.0.0 /bin/bash
