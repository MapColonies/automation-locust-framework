import json
import os
import sys
from pathlib import Path

from locust import (
    between,
    constant,
    constant_pacing,
    events,
    task, HttpUser,
)

from common.config.config import WmtsConfig, config_obj, ElevationConfig

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

stat_file = open("stats.csv", "w")
positions_list_path = ElevationConfig.positions_path
print(positions_list_path)


# def set_wait_time(timer_selection, wait_time):
#     if timer_selection == 1:
#         return constant(wait_time), CONSTANT_TIMER_STR
#     elif timer_selection == 2:
#         return constant_throughput(wait_time), CONSTANT_THROUGHPUT_TIMER_STR
#     elif timer_selection == 3:
#         return (
#             between(config_obj["wmts"].MIN_WAIT, config_obj["wmts"].MAX_WAIT),
#             BETWEEN_TIMER_STR,
#         )
#     elif timer_selection == 4:
#         return constant_pacing(wait_time), CONSTANT_PACING_TIMER_STR
#     else:
#         return None, INVALID_TIMER_STR


class User(HttpUser):
    # timer_selection = config_obj["wmts"].WAIT_TIME_FUNC[0]
    wait_time = 1

    # wait_time, timer_message = set_wait_time(timer_selection, wait_time)
    # print(timer_message)

    def on_start(self):
        if ElevationConfig.request_type == "json":
            with open(positions_list_path, 'r') as file:
                self.request_body = json.load(file)
                print(self.request_body)
        elif ElevationConfig.request_type == "protobuf":
            with open(positions_list_path, 'rb') as file:
                self.request_body = file.read()
                print(self.request_body)
        else:
            return FileNotFoundError

    @task(1)
    def index(self):
        self.client.post(
            "/",
            data=self.request_body,
            verify=False,
            headers=ElevationConfig.headers
        )

    def on_stop(self):
        pass
        # rsp_list = extract_response_time_from_record(
        #     csv_path=config_obj["wmts"].REQUESTS_RECORDS_CSV
        # )
        # percentile_rages_dict = {}
        # rsp_time_ranges = [(0, 100), (101, 500), (501, None)]
        # for idx, rsp_t_range in enumerate(rsp_time_ranges):
        #     counter = count_rsp_time_by_rsp_time_ranges(
        #         rsp_time_data=rsp_list, rsp_range=rsp_t_range
        #     )

        #     percentile = get_percentile_value(
        #         rsp_counter=counter, rsp_time_list=rsp_list
        #     )
        #     percentile_rages_dict[str(rsp_time_ranges[idx])] = percentile
        # write_rsp_time_percentile_ranges(percentile_rages_dict)


@events.request.add_listener
def hook_request_(
        request_type, name, response_time, response_length, response, **kw
):
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
