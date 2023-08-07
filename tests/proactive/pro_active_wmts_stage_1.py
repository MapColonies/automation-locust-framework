from locust import (
    HttpUser,
    between,
    constant,
    constant_pacing,
    constant_throughput,
    task,
)
from common.utils.csvreader import CSVReader

from common.config.config import WmtsConfig, config_obj
from common.utils.constants.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)


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


wmts_csv_path = WmtsConfig.WMTS_CSV_PATH
ssn_reader = CSVReader(wmts_csv_path)


class SizingUser(HttpUser):
    timer_selection = config_obj["default"].WAIT_TIME_FUNC
    wait_time = config_obj["default"].WAIT_TIME

    wait_time, timer_message = set_wait_time(timer_selection, wait_time)
    print(timer_message)

    @task(1)
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

    host = config_obj["wmts"].HOST


# Comment For testing
# Comment For testing 2
