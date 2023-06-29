import json
import os
from locust import HttpUser, events, task

from common.config.config import ElevationConfig
from common.validation.validation_utils import (
    extract_file_type,
    write_rps_percent_results,
)

results_path = os.getcwd()

positions_list_path = ElevationConfig.positions_path

if type(ElevationConfig.percent_ranges) == str:
    percent_ranges = json.loads(ElevationConfig.percent_ranges_counters)
else:
    percent_ranges = ElevationConfig.percent_ranges_counters
print(percent_ranges)


# {(0, 100): 0, (101, 500): 0, (501, None): 0}

class CustomUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_body = None

    def on_start(self):
        print("Test started!")
        request_type = extract_file_type(file_path=positions_list_path)
        if request_type == "json":
            with open(positions_list_path) as file:
                body = json.load(file)
                self.request_body = {"request_type": request_type, "body": body}
        elif request_type == "bin":
            with open(positions_list_path, "rb") as file:
                body = file.read()
                self.request_body = {"request_type": request_type, "body": body}
        else:
            return "invalid file path"

    @task(1)
    def index(self):
        if self.request_body["request_type"] == "json":
            self.client.post(
                "/", json=self.request_body["body"], headers=ElevationConfig.headers
            )
        elif self.request_body["request_type"] == "bin":
            self.client.post(
                "/",
                data=self.request_body["body"],
                headers=ElevationConfig.headers,
            )

        # Process the response as needed

    def on_stop(self):
        # Calculate and present the percentage results
        percent_value_by_range = {}
        for k in counters:
            percent_range = (counters[k] / total_requests) * 100
            percent_value_by_range[f"{k}"] = percent_range
        print(percent_value_by_range)
        percent_value_by_range["total_requests"] = total_requests
        write_rps_percent_results(
            custom_path=results_path, percente_value_by_range=percent_value_by_range
        )


# Define the response time counters
counters = percent_ranges
print(counters, "this is the counters")
# print("counters is  ---- ", counters)
total_requests = 0


# Define the response time ranges
# range_1 = (0, 100)
# range_2 = (101, 500)
# range_3 = (501, None)


# x = {"range_1":(0, 100), "range_2":(101, 500), "range_3":(501, None) }
# Define the response time event hook
@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters, total_requests
    print(response_time)
    print(counters)
    for k in counters:
        print(k, "check ranges for counters")
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
