import os
import sys

# sys.path.append(myDir)
from locust import (
    HttpUser,
    between,
    constant,
    constant_pacing,
    constant_throughput,
    task,
)

from common.config.config import config_obj
from common.data_modules.get_all_layer import create_layers_urls
from common.utils.constants.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)

myDir = os.getcwd()
sys.path.insert(0, "../..")
print(myDir)




def set_wait_time(timer_selection, wait_time):
    if timer_selection == 1:
        return constant(wait_time), CONSTANT_TIMER_STR
    elif timer_selection == 2:
        return constant_throughput(wait_time), CONSTANT_THROUGHPUT_TIMER_STR
    elif timer_selection == 3:
        return (
            between(config_obj["default"].MIN_WAIT, config_obj["default"].MAX_WAIT),
            BETWEEN_TIMER_STR,
        )
    elif timer_selection == 4:
        return constant_pacing(wait_time), CONSTANT_PACING_TIMER_STR
    else:
        return None, INVALID_TIMER_STR


class SizingUser(HttpUser):
    timer_selection = config_obj["default"].WAIT_TIME_FUNC
    wait_time = config_obj["default"].WAIT_TIME

    wait_time, timer_message = set_wait_time(timer_selection, wait_time)

    def on_start(self):
        self.layers_tiles_urls = create_layers_urls()
        # print("on start function")

    @task(1)
    def index(self):
        for layer_urls in self.layers_tiles_urls:
            for tile_url in layer_urls:
                self.client.get(
                    f"{tile_url}", headers={"Cache-Control": "no-cache"}, verify=False
                )

    host = config_obj["default"].HOST
