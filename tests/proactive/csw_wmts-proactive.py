import os
import random
import sys
from pathlib import Path

from common.data_modules.random_tiles_generator import create_random_layers_urls
from tests.pycsw.test_data.queries import POLYGON_XML, ID_RECORD_XML, REGION_RECORD_XML

myDir = os.getcwd()
sys.path.insert(0, '../..')
print(myDir)
# sys.path.append(myDir)

from locust import (
    HttpUser,
    between,
    constant,
    constant_pacing,
    task
)

from common.config.config import config_obj, ProActiveConfig, Config
from common.utils.constants.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)

myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a = str(path.parent.absolute())
sys.path.append(a)


def set_wait_time(timer_selection, wait_time):
    if timer_selection == 1:
        return constant(wait_time), CONSTANT_TIMER_STR
    elif timer_selection == 2:
        pass
        # return constant_throughput(wait_time), CONSTANT_THROUGHPUT_TIMER_STR
    elif timer_selection == 3:
        return (
            between(config_obj["default"].MIN_WAIT, config_obj["default"].MAX_WAIT),
            BETWEEN_TIMER_STR,
        )
    elif timer_selection == 4:
        return constant_pacing(wait_time), CONSTANT_PACING_TIMER_STR
    else:
        return None, INVALID_TIMER_STR


class PycswInquiries(HttpUser):
    pycsw_host = ProActiveConfig.pyscw_host

    @task(1)
    def get_records_by_polygon(self):
        self.client.post(
            "/",
            data=POLYGON_XML.encode("UTF-8"),
            params={"token": Config.TOKEN},
            verify=False,
        )

    @task(1)
    def get_records_by_id(self):
        self.client.post(
            "/",
            data=ID_RECORD_XML.encode("utf-8"),
            params={"token": Config.TOKEN},
            verify=False,
        )

    @task(1)
    def get_records_by_region(self):
        self.client.post(
            "/",
            data=REGION_RECORD_XML.encode("utf-8"),
            params={"token": Config.TOKEN},
            verify=False,
        )


class WmtsInquiries(HttpUser):
    wmts_host = ProActiveConfig.wmts_host

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.random_layers_tiles_urls = None

    @task
    def wmts_requests(self):
        # Task 2 logic goes here
        for layer_urls in self.random_layers_tiles_urls:
            for tile_url in layer_urls:
                self.client.get(f"{tile_url}", headers={"Cache-Control": "no-cache"}, verify=False)


class MyLocust(HttpUser):
    tasks = {WmtsInquiries: 1, PycswInquiries: 1}

    # Common tasks for all user behaviors can be defined here

    def on_start(self):
        # Logic to execute when a user starts a task
        self.random_layers_tiles_urls = create_random_layers_urls()
        random.shuffle(self.random_layers_tiles_urls)


