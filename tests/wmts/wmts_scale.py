import os
import sys
from config.config import WmtsConfig, config_obj
from locust import HttpUser, between, constant, constant_pacing, constant_throughput, task, events, tag, FastHttpUser
from locust_plugins.csvreader import CSVReader

wmts_csv_path_up_scale = WmtsConfig.WMTS_CSV_PATH_UPSCALE

upscale_reader = CSVReader(wmts_csv_path_up_scale)


class User(FastHttpUser):
    between(1, 1)

    @task(1)  # #WMTS - “HTTP_REQUEST_TYPE /SUB_DOMAIN/PROTOCOL/LAYER/TILE_MATRIX_SET/Z/X/Y.IMAGE_FORMAT HTTP_VERSION“
    @tag("WMTS-UpScale")
    def index(self):
        points = next(upscale_reader)
        if config_obj["wmts"].TOKEN is None:
            self.client.get(
                f"/{config_obj['wmts'].LAYER_TYPE_UPSCALE}/"
                f"{config_obj['wmts'].LAYER_NAME_UPSCALE}/"
                f"{config_obj['wmts'].GRID_NAME_UPSCALE}/"
                f"{points[0]}/{points[1]}/{points[2]}"
                f"{config_obj['wmts'].IMAGE_FORMAT_UPSCALE}",
            )
        else:
            self.client.get(
                f"/{config_obj['wmts'].LAYER_TYPE_UPSCALE}/"
                f"{config_obj['wmts'].LAYER_NAME_UPSCALE}/"
                f"{config_obj['wmts'].GRID_NAME_UPSCALE}/"
                f"{points[0]}/{points[1]}/{points[2]}"
                f"{config_obj['wmts'].IMAGE_FORMAT_UPSCALE}"
                f"?token={config_obj['wmts'].TOKEN}",
            )

    host = 'https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1'
