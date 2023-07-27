import random

from locust import HttpUser, constant, events, task

from common.config.config import ElevationConfig
from common.utils.data_generator.data_utils import generate_points_request
from common.validation.validation_utils import (
    initiate_counters_by_ranges,
    retype_env,
    write_rps_percent_results,
)

if isinstance(ElevationConfig.percent_ranges, str):
    percent_ranges = retype_env(ElevationConfig.percent_ranges)
else:
    percent_ranges = ElevationConfig.percent_ranges

reports_path = ElevationConfig.results_path

ranges = [tup[1] for tup in percent_ranges]

polygons = retype_env(ElevationConfig.poly)


class CustomUser(HttpUser):
    response_times = []
    wait_time = constant(int(ElevationConfig.wait_time))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.avg_response_time = None
        self.points_amount_range = ElevationConfig.points_amount_range
        self.points_amount = random.randint(0, self.points_amount_range)
        self.poly = random.choice(polygons)

    @task(1)
    def index(self):
        body = generate_points_request(
            points_amount=self.points_amount, poly=self.poly, payload_flag=True
        )
        if retype_env(ElevationConfig.token_flag):
            self.client.post(
                f"?token={ElevationConfig.TOKEN}",
                json=body,
                headers={"Content-Type": "application/json"},
            )

        else:
            self.client.post(
                "/",
                json=body,
                headers={"Content-Type": "application/json"},
                verify=False,
            )


counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
total_requests = 0
test_results = []
response_time_data = []
points_amount_avg_rsp = []
avg_response_time = 0


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters, total_requests
    for index, value in enumerate(ranges[:-1]):
        if value > response_time:
            counters[f"counter{index + 1}"] += 1
            break
    if ranges[-2] < response_time:
        counters[f"counter{len(ranges)}"] += 1
    total_requests += 1


@events.test_start.add_listener
def reset_counters(**kwargs):
    global counters, total_requests, response_time_data
    counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
    total_requests = 0
    response_time_data = []


@events.test_stop.add_listener
def on_locust_stop(environment, **kwargs):
    global total_requests, counters
    percent_value_by_range = {}
    for index, (key, value) in enumerate(counters.items()):
        percent_range = (value / total_requests) * 100
        percent_value_by_range[f"{percent_ranges[index]}"] = percent_range

    percent_value_by_range["total_requests"] = total_requests
    write_rps_percent_results(
        custom_path=ElevationConfig.results_path,
        percent_value_by_range=percent_value_by_range,
    )


# Run the Locust test
class MyUser(CustomUser):
    wait_time = constant(int(ElevationConfig.wait_time))
