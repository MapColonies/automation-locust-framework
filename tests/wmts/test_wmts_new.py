import logging
import os
import sys

# Use Enum for timer selection
from enum import Enum
from pathlib import Path

from locust import (
    FastHttpUser,
    between,
    constant,
    constant_pacing,
    constant_throughput,
    events,
    task,
)
from locust_plugins.csvreader import CSVReader

# Assuming you have a separate config.py file containing WmtsConfig and config_obj
from common.config.config import WmtsConfig, config_obj

# TODO: Check it why missing how it moved
from common.utils import (
    count_rsp_time_by_rsp_time_ranges,
    extract_response_time_from_record,
    get_percentile_value,
    write_rsp_time_percentile_ranges,
)
from common.utils.constants.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)


class TimerSelection(Enum):
    CONSTANT = 1
    CONSTANT_THROUGHPUT = 2
    BETWEEN = 3
    CONSTANT_PACING = 4


myDir = os.getcwd()
sys.path.append(myDir)

path = Path(myDir)
a = str(path.parent.absolute())
sys.path.append(a)

stat_file = open("stats.csv", "w")
wmts_csv_path = WmtsConfig.WMTS_CSV_PATH
ssn_reader = CSVReader(wmts_csv_path)


def set_wait_time(timer_selection, wait_time):
    if timer_selection == TimerSelection.CONSTANT:
        return constant(wait_time), CONSTANT_TIMER_STR
    elif timer_selection == TimerSelection.CONSTANT_THROUGHPUT:
        return constant_throughput(wait_time), CONSTANT_THROUGHPUT_TIMER_STR
    elif timer_selection == TimerSelection.BETWEEN:
        return (
            between(config_obj["wmts"].MIN_WAIT, config_obj["wmts"].MAX_WAIT),
            BETWEEN_TIMER_STR,
        )
    elif timer_selection == TimerSelection.CONSTANT_PACING:
        return constant_pacing(wait_time), CONSTANT_PACING_TIMER_STR
    else:
        return None, INVALID_TIMER_STR


class User(FastHttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer_selection = config_obj["wmts"].WAIT_TIME_FUNC[0]
        self.wait_time = config_obj["wmts"].WAIT_TIME[0]
        self.wait_time, self.timer_message = set_wait_time(
            self.timer_selection, self.wait_time
        )
        logging.info(self.timer_message)

    @task(1)
    def index(self):
        points = next(ssn_reader)
        url = (
            f"/{config_obj['wmts'].LAYER_TYPE}/"
            f"{config_obj['wmts'].LAYER_NAME}/"
            f"{config_obj['wmts'].GRID_NAME}/"
            f"{points[0]}/{points[1]}/{points[2]}"
            f"{config_obj['wmts'].IMAGE_FORMAT}"
        )
        if config_obj["wmts"].TOKEN:
            url += f"?token={config_obj['wmts'].TOKEN}"
        self.client.get(url)

    host = config_obj["wmts"].HOST

    def on_stop(self):
        rsp_list = extract_response_time_from_record(
            csv_path=config_obj["wmts"].REQUESTS_RECORDS_CSV
        )
        percentile_rages_dict = {}
        rsp_time_ranges = [(0, 100), (101, 500), (501, None)]
        for idx, rsp_t_range in enumerate(rsp_time_ranges):
            counter = count_rsp_time_by_rsp_time_ranges(
                rsp_time_data=rsp_list, rsp_range=rsp_t_range
            )
            percentile = get_percentile_value(
                rsp_counter=counter, rsp_time_list=rsp_list
            )
            percentile_rages_dict[str(rsp_time_ranges[idx])] = percentile
        write_rsp_time_percentile_ranges(percentile_rages_dict)


@events.request.add_listener
def hook_request_(request_type, name, response_time, response_length, response, **kw):
    stat_file.write(
        str(response)
        + ";"
        + request_type
        + ";"
        + name
        + ";"
        + str(response_time)
        + ";"
        + str(response_length)
        + "\n"
    )


@events.quitting.add_listener
def hook_quitting(environment, **kw):
    stat_file.close()
