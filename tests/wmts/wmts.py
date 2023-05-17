import os
import sys
from config.config import WmtsConfig, config_obj
from locust import HttpUser, between, constant, constant_pacing, constant_throughput, task, events, tag, FastHttpUser
from locust_plugins.csvreader import CSVReader
from pathlib import Path
from utils.percentile_calculation import calculate_times, generate_name
from common.strings import BETWEEN_TIMER_STR, CONSTANT_PACING_TIMER_STR, CONSTANT_THROUGHPUT_TIMER_STR, \
    CONSTANT_TIMER_STR, INVALID_TIMER_STR
import time

myDir = os.getcwd()
sys.path.append(myDir)
files = os.listdir(myDir)
print(str(myDir))
path = Path(myDir)
# a = str(path.parent.absolute())
# sys.path.append(a)


wmts_csv_path = WmtsConfig.WMTS_CSV_PATH

file_name = generate_name(__name__)
stat_file = open(f"{config_obj['wmts'].root_dir}/{file_name}", 'w')

ssn_reader = CSVReader(wmts_csv_path)


class User(FastHttpUser):
    between(1, 1)

    @task(1)  # #WMTS - “HTTP_REQUEST_TYPE /SUB_DOMAIN/PROTOCOL/LAYER/TILE_MATRIX_SET/Z/X/Y.IMAGE_FORMAT HTTP_VERSION“
    @tag("wmts-loading")
    def index(self):
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
