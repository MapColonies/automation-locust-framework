# import os
# import sys
# from pathlib import Path
#
# myDir = os.getcwd()
# sys.path.append(myDir)
#
# path = Path(myDir)
# a = str(path.parent.absolute())
# sys.path.append(a)
import json
import os
import threading

from locust import HttpUser, constant, events, task

from common.config.config import config_obj
from common.utils.csvreader import CSVReader
from common.validation.validation_utils import (
    find_range_for_response_time,
    initiate_counters_by_ranges,
    read_tests_data_folder,
    retype_env,
    write_rps_percent_results,
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
    wait_time = constant(wait_time)

    @task(1)
    def index(self):
        url = next(ssn_reader)

        self.client.get(url=url[1], verify=False)

        host = config_obj["default"].HOST


# create counters for each range value from the configuration
counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
total_requests = 0
test_results = []
response_time_data = []
points_amount_avg_rsp = []
avg_response_time = 0


@events.test_start.add_listener
def on_locust_init(environment, **_kwargs):
    environment.users_count = environment.runner.target_user_count


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters, total_requests
    counters = find_range_for_response_time(
        response_time=response_time, ranges_list=percent_ranges, counters_dict=counters
    )
    total_requests += 1


@events.test_stop.add_listener
def log_counters(environment):
    global counters
    worker_id = os.environ.get("HOSTNAME")
    print(worker_id)
    filename = f"{results_path}/workers_reports/results_{worker_id}.json"
    counters["total_requests"] = total_requests
    json_object = json.dumps(counters)
    with open(filename, "w") as outfile:
        outfile.write(json_object)
    outfile.close()


@events.test_start.add_listener
def reset_counters(**kwargs):
    global counters, total_requests, run_number, start_time_data, response_time_data
    counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
    total_requests = 0
    start_time_data = []
    response_time_data = []


@events.test_stop.add_listener
def on_locust_stop(environment, **kwargs):
    """
    The percent calculation for each range by range counters
    after calculate the percent value with the result into json file
    :return:
    """
    workers_data = read_tests_data_folder(folder_path=f"{results_path}/workers_reports")
    print(workers_data)
    sum_dict = sum_nested_dicts(workers_data)
    # global total_requests, counters
    percent_value_by_range = {}
    total_requests1 = sum_dict["total_requests"]
    if total_requests != 0:
        for index, (key, value) in enumerate(sum_dict.items()):
            percent_range = (value / total_requests1) * 100
            percent_value_by_range[f"{key}"] = percent_range

        percent_value_by_range["total_requests"] = int(total_requests1)
        print(percent_value_by_range)
        write_rps_percent_results(
            custom_path=results_path,
            percent_value_by_range=percent_value_by_range,
        )

    else:
        print(
            "The test execution failed - requests did not proceed. Check the logs to find the problem"
        )
