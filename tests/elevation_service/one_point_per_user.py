import json
import os
from locust import HttpUser, events, task

from common.config.config import ElevationConfig
from common.validation.validation_utils import (
    write_rps_percent_results, get_request_parameters, extract_points_from_json, initiate_counters_by_ranges,
)

positions_list_path = ElevationConfig.positions_path

if type(ElevationConfig.percent_ranges) == str:
    percent_ranges = list(ElevationConfig.percent_ranges)
else:
    percent_ranges = ElevationConfig.percent_ranges


# request_body = get_request_parameters(positions_list_path=positions_list_path)

positions_bodies = extract_points_from_json(json_file=positions_list_path)
# print(positions_bodies)


class CustomUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_bodies = positions_bodies
        self.bodies_length = len(self.request_bodies)
        self.index = 0


    @task(1)
    def index(self):
        body = self.request_bodies[self.index]
        print(self.index , body)
        # if self.request_bodies["request_type"] == "json":
        self.client.post(
            "/", json=body, headers={'Content-Type': 'application/json'}
        )
        self.index += 1
        # elif self.request_bodies["request_type"] == "bin":
        #     self.client.post(
        #         "/",
        #         data=self.request_bodies["body"],
        #         headers=self.request_bodies["header"],
        #     )

        # Process the response as needed

    def on_stop(self):
        # Calculate and present the percentage results
        percent_value_by_range = {}
        for index, (key, value) in enumerate(counters.items()):
            percent_range = (value / total_requests) * 100
            percent_value_by_range[f"{percent_ranges[index]}"] = percent_range

        percent_value_by_range["total_requests"] = total_requests
        write_rps_percent_results(
            custom_path=ElevationConfig.results_path, percente_value_by_range=percent_value_by_range
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
# todo:ask alex which wait time to set to insure that we create the next task only if we get reponse from the first task
# todo: check the ranges validation - json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
