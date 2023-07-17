import datetime
import json
from itertools import cycle

from locust import HttpUser, constant, events, task

from common.config.config import ElevationConfig
from common.validation.validation_utils import (
    create_custom_graph,
    create_start_time_response_time_graph,
    extract_points_from_json,
    initiate_counters_by_ranges,
    write_rps_percent_results,
)

positions_list_path = ElevationConfig.positions_path

if type(ElevationConfig.percent_ranges) == str:
    percent_ranges = list(ElevationConfig.percent_ranges)
else:
    percent_ranges = ElevationConfig.percent_ranges

positions_bodies = extract_points_from_json(json_file=positions_list_path)

reports_path = ElevationConfig.results_path


class CustomUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_results = []
        self.request_bodies = positions_bodies
        self.request_bodies_cycle = cycle(self.request_bodies)
        self.graph_name = ElevationConfig.graph_name
        self.users_count = None
        self.req_start_t_rsp_t = []

    @task(1)
    def index(self):
        body = json.loads(next(self.request_bodies_cycle))
        # if self.request_bodies["request_type"] == "json":
        self.client.post(
            "/", json=body, headers={"Content-Type": "application/json"}, verify=False
        )
        # elif self.request_bodies["request_type"] == "bin":
        #     self.client.post(
        #         "/",
        #         data=self.request_bodies["body"],
        #         headers=self.request_bodies["header"],
        #     )
        self.users_count = self.environment.runner.user_count

    def on_stop(self):
        average_response_time = self.environment.runner.stats.total.avg_response_time
        self.test_results.append(
            {"users": self.users_count, "avg_response_time": average_response_time}
        )
        # print(self.test_results)
        create_custom_graph(
            graph_name="Users_vs_AvgResponseTime",
            graph_path=reports_path,
            test_results=self.test_results,
            graph_title=None,
            rotation=None,
        )

        # self.req_start_t_rsp_t = create_graph_results_data_format(["start_time", "response_time"],
        #                                                           [])
        # print(self.req_start_t_rsp_t)
        create_start_time_response_time_graph(
            graph_name=f"RequestStartTime_vs_ResponseTime-{run_number}",
            start_time_data=start_time_data,
            response_time_data=response_time_data,
        )

        # percent_value_by_range = {}
        # if total_requests != 0:
        #     for index, (key, value) in enumerate(counters.items()):
        #         range_percent_val = (value / total_requests) * 100
        #         percent_value_by_range[f"{percent_ranges[index]}"] = range_percent_val
        #     percent_value_by_range["total_requests"] = total_requests
        #     write_rps_percent_results(
        #         custom_path=reports_path, percente_value_by_range=percent_value_by_range
        #     )
        # else:
        #     percent_value_by_range["total_requests"] = total_requests


counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
total_requests = 0
run_number = 0
start_time_data = []
response_time_data = []
file_created = False


@events.request.add_listener
def on_request(response_time, **kwargs):
    start_time = datetime.datetime.fromtimestamp(kwargs["start_time"])
    response_time_data.append(response_time)
    start_time_data.append(start_time)


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters, total_requests

    for index, range_val in enumerate(percent_ranges):
        if range_val[1] is None and response_time >= range_val[0]:
            counters[f"counter{index + 1}"] += 1
        elif range_val[0] <= response_time <= range_val[1]:
            counters[f"counter{index + 1}"] += 1

    total_requests += 1


@events.test_start.add_listener
def reset_counters(**kwargs):
    global counters, total_requests, run_number, start_time_data, response_time_data
    counters = counters
    total_requests = 0
    run_number += 1
    start_time_data = []
    response_time_data = []


# Run the Locust test
class MyUser(CustomUser):
    wait_time = constant(ElevationConfig.wait_time)


@events.test_stop.add_listener
def on_locust_stop(environment, **kwargs):
    global file_created

    # Ensure file creation code is executed only once
    if not file_created:
        percent_value_by_range = {}
        if total_requests != 0:
            for index, (key, value) in enumerate(counters.items()):
                range_percent_val = (value / total_requests) * 100
                percent_value_by_range[f"{percent_ranges[index]}"] = range_percent_val
            percent_value_by_range["total_requests"] = total_requests
            write_rps_percent_results(
                custom_path=reports_path, percente_value_by_range=percent_value_by_range
            )
        else:
            percent_value_by_range["total_requests"] = total_requests
