import json
from locust import HttpUser, events, task

from common.config.config import ElevationConfig, Config
from common.validation.validation_utils import (
    write_rps_percent_results, get_request_parameters, read_tests_data_folder, initiate_counters_by_ranges,
)

results_path = ElevationConfig.results_path

positions_list_path = ElevationConfig.positions_path

if type(ElevationConfig.percent_ranges) == str:
    percent_ranges = list(ElevationConfig.percent_ranges)
else:
    percent_ranges = ElevationConfig.percent_ranges

request_body = get_request_parameters(positions_list_path=positions_list_path)

request_data_bodies = read_tests_data_folder(folder_path=ElevationConfig.bulks_root_folder)


class CustomUser(HttpUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_body = request_body
        # bulks_amount = ElevationConfig.bulks_amount  # Number of tasks per user, configurable
        bulks_amount = len(request_data_bodies)
        self.tasks_per_user = request_data_bodies

    task(1)

    def index(self):
        for file_name, body in self.tasks_per_user.items():
            if "json" in file_name:
                self.client.post(
                    "/", json=body, headers={"Content-Type": "application/json"}
                )
            elif "bin" in file_name:
                self.client.post(
                    "/",
                    data=body,
                    headers={"Content-Type": "application/octet-stream"},
                )
            else:
                return "Invalid file type"
                # Process the response as needed

    def on_stop(self):
        # Calculate and present the percentage results
        percent_value_by_range = {}
        for k in counters:
            percent_range = (counters[k] / total_requests) * 100
            percent_value_by_range[f"{k}"] = percent_range

        percent_value_by_range["total_requests"] = total_requests
        write_rps_percent_results(
            custom_path=results_path, percente_value_by_range=percent_value_by_range
        )



counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
total_requests = 0


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters, total_requests

    for index, range in enumerate(percent_ranges):
        if range[1] is None and response_time >= range[0]:
            counters[f"counter{index + 1}"] += 1
        elif range[0] <= response_time <= range[1]:
            counters[f"counter{index + 1}"] += 1

    total_requests += 1


@events.test_start.add_listener
def reset_counters(**kwargs):
    global counters, total_requests
    counters = counters
    total_requests = 0


# Run the Locust test
class MyUser(CustomUser):
    min_wait = 100
    max_wait = 1000
