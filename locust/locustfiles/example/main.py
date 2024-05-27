# # -*- coding: utf-8 -*-
#
# from locust import HttpUser, task, between
# from lib.example_functions import choose_random_page
#
#
# default_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
#
#
# class WebsiteUser(HttpUser):
#     wait_time = between(1, 2)
#
#     @task(1)
#     def get_index(self):
#         self.client.get("/", headers=default_headers)
#
#     @task(3)
#     def get_random_page(self):
#         self.client.get(choose_random_page(), headers=default_headers)
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

from lib.common.config.config import config_obj
from lib.common.utils.csvreader import CSVReader
from lib.common.utils.data_generator.data_utils import custom_sorting_key
from lib.common.validation.validation_utils import (
    find_range_for_response_time,
    initiate_counters_by_ranges,
    read_tests_data_folder,
    retype_env,
    write_rps_percent_results,
)

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

# ssn_reader = CSVReader(config_obj["_3d"].CSV_DATA_PATH)
ssn_reader = CSVReader(
    "/home/shayavr/Desktop/git/automation-locust-framework/scripts/extract_urls_script_3d/filtered_urls.csv")
results_path = config_obj["_3d"].RESULTS_PATH

if isinstance(config_obj["wmts"].WAIT_TIME, str):
    wait_time = retype_env(config_obj["wmts"].WAIT_TIME)
else:
    wait_time = config_obj["wmts"].WAIT_TIME

file_lock = threading.Lock()

stats = {"total_requests": 0}
counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
print(counters)
counters_keys = list(counters.keys())


class User(HttpUser):
    wait_time = constant(wait_time)

    @task(1)
    def index(self):
        url = next(ssn_reader)
        with self.client.get(url=url[1], verify=False, catch_response=True) as response:
            content_type = response.headers.get("Content-Type", "")
            if content_type != "application/octet-stream":
                response.failure(f"Invalid response content-type: {content_type}")
            elif response.status_code == 402 or response.status_code == 403 or response.status_code == 401:
                response.failure(f"status code: {response.status_code} for: {url[1]}")

        host = config_obj["default"].HOST


@events.init.add_listener
def locust_init(environment, **kwargs):
    """
    We need somewhere to store the stats.
    On the master node stats will contain the aggregated sum of all content-lengths,
    while on the worker nodes this will be the sum of the content-lengths since the
    last stats report was sent to the master
    """
    if environment.web_ui:
        # this code is only run on the master node (the web_ui instance doesn't exist on workers)
        @environment.web_ui.app.route("/total_requests")
        def total_content_length():
            """
            Add a route to the Locust web app, where we can see the total content-length
            """
            requests_amount = stats["total_requests"]
            percent_value_by_range = {}
            print(counters)

            if requests_amount != 0:
                for index, (key, value) in enumerate(counters.items()):
                    percent_range = (value / requests_amount) * 100
                    percent_value_by_range[f"{key}"] = percent_range

                # percent_value_by_range["total_requests"] = int(requests_amount)
                # print(percent_value_by_range)
                percent_value_by_range = dict(sorted(percent_value_by_range.items(), key=custom_sorting_key))
            return {"percent_value": percent_value_by_range,
                    "total_requests": stats["total_requests"]}


# create counters for each range value from the configuration


@events.test_start.add_listener
def on_locust_init(environment, **_kwargs):
    environment.users_count = environment.runner.target_user_count


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters
    print("percent_ranges is", percent_ranges)
    counters = find_range_for_response_time(
        response_time=response_time, ranges_list=percent_ranges, counters_dict=counters
    )
    # total_requests += 1
    stats["total_requests"] += 1


@events.report_to_master.add_listener
def on_report_to_master(client_id, data):
    """
    This event is triggered on the worker instances every time a stats report is
    to be sent to the locust master. It will allow us to add our extra content-length
    data to the dict that is being sent, and then we clear the local stats in the worker.
    """
    data["total_requests"] = stats["total_requests"]
    for range_val in counters_keys:
        data[range_val] = counters[range_val]
        counters[range_val] = 0
    stats["total_requests"] = 0
    # counters["total_requests"] = 0


@events.worker_report.add_listener
def on_worker_report(client_id, data):
    """
    This event is triggered on the master instance when a new stats report arrives
    from a worker. Here we just add the content-length to the master's aggregated
    stats dict.
    """
    stats["total_requests"] += data["total_requests"]
    for range_val in counters_keys:
        counters[range_val] += data[range_val]
    print(stats)
    print(data)


@events.test_start.add_listener
def reset_counters(**kwargs):
    global counters, total_requests, stats
    counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
    total_requests = 0
    stats = {"total_requests": 0}
