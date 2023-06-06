import json
import os
import sys
from pathlib import Path

from locust import User, task, events, HttpUser, constant, constant_throughput, between, constant_pacing

from common.config.config import ElevationConfig, config_obj
from common.utils.constants.strings import CONSTANT_TIMER_STR, CONSTANT_THROUGHPUT_TIMER_STR, BETWEEN_TIMER_STR, \
    CONSTANT_PACING_TIMER_STR, INVALID_TIMER_STR
from common.validation.validation_utils import extract_file_type, write_rps_percent_results

myDir = os.getcwd()
sys.path.append(myDir)

path = Path(myDir)
a = str(path.parent.absolute())
sys.path.append(a)

positions_list_path = ElevationConfig.positions_path
results_path = ElevationConfig.results_path


class CustomUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_body = None

    def on_start(self):
        request_type = extract_file_type(file_path=positions_list_path)
        if request_type == "json":
            with open(positions_list_path, 'r') as file:
                body = json.load(file)
                self.request_body = {"request_type": request_type, "body": body}
        elif request_type == "bin":
            with open(positions_list_path, 'rb') as file:
                body = file.read()
                self.request_body = {"request_type": request_type, "body": body}
        else:
            return "invalid file path"

    @task(1)
    def index(self):
        if self.request_body["request_type"] == "json":
            self.client.post(
                "/",
                json=self.request_body["body"],
                headers=ElevationConfig.headers
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
        percent_range_1 = (counter_range_1 / total_requests) * 100
        percent_range_2 = (counter_range_2 / total_requests) * 100
        percent_range_3 = (counter_range_3 / total_requests) * 100

        percent_value_by_range = {f"{range_1}": f"{percent_range_1}%",
                                  f"{range_2}": f"{percent_range_2}%",
                                  f"{range_3}": f"{percent_range_3}%",
                                  "total_requests": f"{total_requests}"}
        write_rps_percent_results(custome_path=results_path, percente_value_by_range=percent_value_by_range)



# Define the response time counters
counter_range_1 = 0
counter_range_2 = 0
counter_range_3 = 0
total_requests = 0

# Define the response time ranges
range_1 = (0, 100)
range_2 = (101, 500)
range_3 = (501, None)


# Define the response time event hook
@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counter_range_1, counter_range_2, counter_range_3, total_requests

    if range_1[0] <= response_time <= range_1[1]:
        counter_range_1 += 1
    elif range_2[0] <= response_time <= range_2[1]:
        counter_range_2 += 1
    elif response_time >= range_3[0]:
        counter_range_3 += 1

    total_requests += 1


@events.test_start.add_listener
def reset_counters(**kwargs):
    global counter_range_1, counter_range_2, counter_range_3, total_requests

    counter_range_1 = 0
    counter_range_2 = 0
    counter_range_3 = 0
    total_requests = 0


# Run the Locust test
class MyUser(CustomUser):
    min_wait = 100
    max_wait = 1000
