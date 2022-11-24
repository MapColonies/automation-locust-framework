import logging
import time

from locust import between
from locust import constant
from locust import constant_pacing
from locust import constant_throughput
from locust import HttpUser
from locust import task
from locust_plugins import StopUser
from locust_plugins.csvreader import CSVReader

import common.config as cfg

logging.error("Reading CSV file")
ssn_reader = CSVReader("csv_data/data/wmts_shaziri.csv")


class SizingUser(HttpUser):
    timer_selection = config_obj["default"].WAIT_TIME_FUNC
    wait_time = config_obj["default"].WAIT_TIME
    if timer_selection == 1:
        wait_time = constant(wait_time)
        print(CONSTANT_TIMER_STR)
    elif timer_selection == 2:
        wait_time = constant_throughput(wait_time)
        print(CONSTANT_THROUGHPUT_TIMER_STR)
    elif timer_selection == 3:
        wait_time = between(
            config_obj["default"].MIN_WAIT, config_obj["default"].MAX_WAIT
        )
        print(BETWEEN_TIMER_STR)
    elif timer_selection == 4:
        wait_time = constant_pacing(wait_time)
        print(CONSTANT_PACING_TIMER_STR)
    else:
        print(INVALID_TIMER_STR)

    @task(1)
    def index(self):
        points = next(ssn_reader)
        self.client.get(
            f"/{cfg.LAYER_TYPE}/{cfg.LAYER}/{cfg.GRIDNAME}/{points[0]}/{points[1]}/{points[2]}{cfg.IMAGE_FORMAT}?token={cfg.TOKEN}",
            verify=False,
        )

    host = cfg.HOST
