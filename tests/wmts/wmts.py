import os
import sys
from config.config import WmtsConfig, config_obj
from locust import HttpUser, between, constant, constant_pacing, constant_throughput, task, events, tag, FastHttpUser
from locust_plugins.csvreader import CSVReader
from pathlib import Path
from utils.ClientX import HttpxUser
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

wmts_csv_path_up_scale = WmtsConfig.WMTS_CSV_PATH_UPSCALE

file_name = generate_name(__name__)
stat_file = open(f"{config_obj['wmts'].root_dir}/{file_name}", 'w')
# wmts_csv_path = "/home/shayavr/Desktop/git/automation-locust-framework/csv_data/data/wmts_shaziri.csv"

ssn_reader = CSVReader(wmts_csv_path)

if config_obj['wmts'].UP_SCALE_FLAG:
    Upscale_reader = CSVReader(wmts_csv_path_up_scale)


class User(HttpxUser):

    timer_selection = config_obj["wmts"].WAIT_TIME_FUNC
    wait_time = config_obj["wmts"].WAIT_TIME
    if isinstance(timer_selection, list) and isinstance(wait_time, list):
        timer_selection = timer_selection[0]
        wait_time = wait_time[0]
    if timer_selection == 1:
        wait_time = constant(wait_time)
        print(CONSTANT_TIMER_STR)
    elif timer_selection == 2:
        wait_time = constant_throughput(wait_time)
        print(CONSTANT_THROUGHPUT_TIMER_STR)
    elif timer_selection == 3:
        wait_time = between(config_obj["wmts"].MIN_WAIT, config_obj["wmts"].MAX_WAIT)
        print(BETWEEN_TIMER_STR)
    elif timer_selection == 4:
        wait_time = constant_pacing(wait_time)
        print(CONSTANT_PACING_TIMER_STR)
    else:
        print(INVALID_TIMER_STR)

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

    @task(2)
    @tag("Wmts-Upscale")
    def up_scale(self):
        if config_obj['wmts'].UP_SCALE_FLAG:
            points = next(Upscale_reader)
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
