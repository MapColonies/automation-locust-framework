import os
import sys
from config.config import WmtsConfig, config_obj
from locust import HttpUser, between, constant, constant_pacing, constant_throughput, task, events, tag, FastHttpUser
from locust_plugins.csvreader import CSVReader
from pathlib import Path
from utils.percentile_calculation import calculate_times, generate_name


myDir = os.getcwd()
sys.path.append(myDir)
files = os.listdir(myDir)
print(str(myDir))
path = Path(myDir)
# a = str(path.parent.absolute())
# sys.path.append(a)

wmts_csv_path = WmtsConfig.WMTS_CSV_PATH
wmts_csv_path_up_scale = WmtsConfig.WMTS_CSV_PATH_UPSCALE

ssn_reader = CSVReader(wmts_csv_path)
upscale_reader = CSVReader(wmts_csv_path_up_scale)

file_name = generate_name(__name__)
stat_file = open(f"{config_obj['wmts'].root_dir}/{file_name}", 'w')
class User(FastHttpUser):
    between(1, 1)

    @task(1)  # #WMTS - “HTTP_REQUEST_TYPE /SUB_DOMAIN/PROTOCOL/LAYER/TILE_MATRIX_SET/Z/X/Y.IMAGE_FORMAT HTTP_VERSION“
    @tag("wmts-loading")
    def index(self):
        if config_obj['wmts'].WMTS_FLAG:
            points = next(ssn_reader)
            if config_obj["wmts"].TOKEN is None:
                self.client.get(
                    f"/{config_obj['wmts'].LAYER_TYPE}/"
                    f"{config_obj['wmts'].LAYER_NAME}/"
                    f"{config_obj['wmts'].GRID_NAME}/"
                    f"{points[0]}/{points[1]}/{points[2]}"
                    f"{config_obj['wmts'].IMAGE_FORMAT}",
                )
            else:
                self.client.get(
                    f"/{config_obj['wmts'].LAYER_TYPE}/"
                    f"{config_obj['wmts'].LAYER_NAME}/"
                    f"{config_obj['wmts'].GRID_NAME}/"
                    f"{points[0]}/{points[1]}/{points[2]}"
                    f"{config_obj['wmts'].IMAGE_FORMAT}"
                    f"?token={config_obj['wmts'].TOKEN}",
                )

    @task(1)
    @tag("Wmts-Upscale")
    def up_scale(self):
        points = next(upscale_reader)
        if config_obj["wmts"].TOKEN is None:
            self.client.get(
                f"/{config_obj['wmts'].LAYER_TYPE}/"
                f"{config_obj['wmts'].LAYER_NAME}/"
                f"{config_obj['wmts'].GRID_NAME}/"
                f"{points[0]}/{points[1]}/{points[2]}"
                f"{config_obj['wmts'].IMAGE_FORMAT}",
            )
        else:
            self.client.get(
                f"/{config_obj['wmts'].LAYER_TYPE}/"
                f"{config_obj['wmts'].LAYER_NAME}/"
                f"{config_obj['wmts'].GRID_NAME}/"
                f"{points[0]}/{points[1]}/{points[2]}"
                f"{config_obj['wmts'].IMAGE_FORMAT}"
                f"?token={config_obj['wmts'].TOKEN}",
            )

    host = 'https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1'

    # host = config_obj["wmts"].HOST
    # host = "http://lb-mapcolonies.gg.wwest.local/mapproxy-ww"

    def on_stop(self):
        calculate_times(file_name, __name__)


@events.request.add_listener
def hook_request_success(request_type, name, response_time, response_length, **kwargs):
    stat_file.write(f"{request_type};{name} ; {response_time};{response_length}  \n")


@events.quitting.add_listener
def hook_quitting(environment, **kw):
    stat_file.close()
