import logging
import os
import sys
from common.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)

myDir = os.getcwd()
sys.path.append(myDir)
from pathlib import Path

path = Path(myDir)
a = str(path.parent.absolute())
sys.path.append(a)

import requests
from config.config import config_obj
from locust import (
    HttpUser,
    between,
    constant,
    constant_pacing,
    constant_throughput,
    task,
)
from locust_plugins.csvreader import CSVReader

# pvc_url = cfg.PVC_HANDLER_ROUTE
# response_param = requests.get(url=f'http://{pvc_url}{config.UPDATE_LAYER_DATA_DIR}/',
#                               params={'file': layers_name})
# "/home/shayavr/Desktop/git/automation-locust/urls_data.csv"
ssn_reader = CSVReader(config_obj["_3d"].CSV_DATA_PATH)


class User(HttpUser):
    timer_selection = config_obj["wmts"].WAIT_TIME_FUNC
    wait_time = config_obj["wmts"].WAIT_TIME
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

    @task(1)
    def index(self):
        url = next(ssn_reader)
        self.client.get(url=url[1], verify=False)

    host = config_obj["default"].HOST
