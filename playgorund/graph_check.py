import os
import threading

from locust import HttpUser, constant, events, task
from common.config.config import config_obj
from common.utils.csvreader import CSVReader
from common.validation.validation_utils import (
    find_range_for_response_time,
    initiate_counters_by_ranges,
    retype_env,
    write_rps_percent_results, set_wait_time,
)
from common.utils.constants.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)
from playgorund.playground import sum_nested_dicts

if isinstance(config_obj["_3d"].percent_ranges, str):
    percent_ranges = retype_env(config_obj["_3d"].percent_ranges)
    percent_ranges.append(0)
    percent_ranges.append(float("inf"))
    percent_ranges = sorted(percent_ranges)
else:
    percent_ranges = config_obj["_3d"].percent_ranges
    percent_ranges.append(0)
    percent_ranges.append(float("inf"))
    percent_ranges = sorted(percent_ranges)

ssn_reader = CSVReader(config_obj["_3d"].CSV_DATA_PATH)
results_path = config_obj["_3d"].RESULTS_PATH

if isinstance(config_obj["wmts"].WAIT_TIME, str):
    wait_time = retype_env(config_obj["wmts"].WAIT_TIME)
else:
    wait_time = config_obj["wmts"].WAIT_TIME

file_lock = threading.Lock()

class User(HttpUser):
    timer_selection = config_obj["wmts"].WAIT_TIME_FUNC
    wait_time_config = config_obj["wmts"].WAIT_TIME
    wait_time, timer_message = set_wait_time(timer_selection, wait_time_config)
    print(timer_message)

    @task(1)
    def index(self):
        url = next(ssn_reader)
        self.client.get(url=url[1], verify=False)

    host = config_obj["default"].HOST


# create counters for each range value from the configuration
counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
total_requests = 0
test_results = []
workers_results = {}


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters, total_requests
    counters = find_range_for_response_time(
        response_time=response_time, ranges_list=percent_ranges, counters_dict=counters
    )
    total_requests += 1
    counters["total_requests"] = total_requests


@events.test_stop.add_listener
def log_counters(environment):
    global counters, workers_results

    worker_id = os.environ.get("HOSTNAME")
    if "master" not in worker_id:
        workers_results[worker_id] = counters
    print("test stop", workers_results)


@events.test_start.add_listener
def reset_counters(**kwargs):
    global counters, total_requests, workers_results
    counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
    total_requests = 0
    workers_results = {}


@events.test_stop.add_listener
def on_locust_stop(environment, **kwargs):
    """
    The percent calculation for each range by range counters
    after calculate the percent value with the result into json file
    :return:
    """
    global workers_results
    print(workers_results)
    sum_dict = sum_nested_dicts(workers_results)
    print(sum_dict)
    percent_value_by_range = {}
    total_request_amount = sum_dict["total_requests"]
    if total_request_amount != 0:
        for index, (key, value) in enumerate(sum_dict.items()):
            percent_range = (value / total_request_amount) * 100
            percent_value_by_range[f"{key}"] = percent_range

        percent_value_by_range["total_requests"] = int(total_request_amount)
        print(percent_value_by_range)
        write_rps_percent_results(
            custom_path=results_path,
            percent_value_by_range=percent_value_by_range,
        )

    else:
        print(
            "The test execution failed - requests did not proceed. Check the logs to find the problem"
        )