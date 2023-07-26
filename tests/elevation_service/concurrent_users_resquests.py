import random
from locust import HttpUser, events, task, constant
from shapely import Polygon
from common.config.config import ElevationConfig
from common.utils.data_generator.data_utils import generate_points_request
from common.validation.validation_utils import (
    write_rps_percent_results, initiate_counters_by_ranges, retype_env)

# todo: remove before delivering
poly = Polygon([(37.75850848099701, -122.50833008408812), (37.75911919711413, -122.49648544907835),
                (37.751620611284935, -122.4937388670471), (37.74863453749236, -122.50742886185911)])

if isinstance(ElevationConfig.percent_ranges, str):
    percent_ranges = retype_env(ElevationConfig.percent_ranges)
else:
    percent_ranges = ElevationConfig.percent_ranges

reports_path = ElevationConfig.results_path

ranges = [tup[1] for tup in percent_ranges]


class CustomUser(HttpUser):
    response_times = []
    wait_time = constant(int(ElevationConfig.wait_time))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.request_body = request_body
        # self.tasks_per_user = request_data_bodies
        self.graph_name = ElevationConfig.graph_name
        self.avg_response_time = None
        self.points_amount_range = ElevationConfig.points_amount_range
        self.points_amount = random.randint(0, self.points_amount_range)
        self.poly = ElevationConfig.poly

    @task(1)
    def index(self):
        body = generate_points_request(points_amount=self.points_amount, poly=poly, payload_flag=True)
        if not retype_env(ElevationConfig.token_flag):
            self.client.post(
                "/", json=body, headers={"Content-Type": "application/json"}, verify=False)
        else:
            self.client.post(
                f"?token={ElevationConfig.TOKEN}", json=body, headers={"Content-Type": "application/json"}
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
        custom_path=ElevationConfig.results_path, percent_value_by_range=percent_value_by_range
    )


# Run the Locust test
class MyUser(CustomUser):
    wait_time = constant(int(ElevationConfig.wait_time))
