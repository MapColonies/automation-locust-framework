#!/bin/bash

docker run -it \
-e input="/opt/terrian_template.json" \
-e output="/opt/blabla.csv" \
-e tiles_number=2 \
-v /home/shayavr/Desktop/scripts_vols/:/opt/ \
terrain_script:v1.0.0 /bin/bash
