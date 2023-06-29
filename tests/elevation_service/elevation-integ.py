import json
import os
from locust import HttpUser, events, task

from common.config.config import ElevationConfig
from common.validation.validation_utils import (
    write_rps_percent_results, get_request_parameters,
)

results_path = os.getcwd()
positions_list_path = ElevationConfig.positions_path

if type(ElevationConfig.percent_ranges) == str:
    percent_ranges = json.loads(ElevationConfig.percent_ranges_counters)
else:
    percent_ranges = ElevationConfig.percent_ranges_counters

request_body = get_request_parameters(positions_list_path=positions_list_path)


class CustomUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_body = request_body

    @task(1)
    def index(self):
        if self.request_body["request_type"] == "json":
            self.client.post(
                "/", json=self.request_body["body"], headers=self.request_body["header"]
            )
        elif self.request_body["request_type"] == "bin":
            self.client.post(
                "/",
                data=self.request_body["body"],
                headers=self.request_body["header"],
            )

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


counters = percent_ranges

total_requests = 0


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters, total_requests

    for k in counters:
        if k[1] is None and response_time >= k[0]:
            counters[k] = counters.get(k, 0) + 1
        elif k[0] <= response_time <= k[1]:
            counters[k] = counters.get(k, 0) + 1

    total_requests += 1


@events.test_start.add_listener
def reset_counters(**kwargs):
    global counters, total_requests
    counters = percent_ranges
    total_requests = 0


# Run the Locust test
class MyUser(CustomUser):
    min_wait = 100
    max_wait = 1000