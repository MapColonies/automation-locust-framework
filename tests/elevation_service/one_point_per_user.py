import datetime
import json
from locust import HttpUser, events, task, constant
from itertools import cycle
from locust.runners import Runner
from matplotlib import pyplot as plt
from common.config.config import ElevationConfig
from common.validation.validation_utils import (
    write_rps_percent_results, extract_points_from_json, create_custom_graph,
    create_start_time_response_time_graph, initiate_counters_by_ranges,
)

positions_list_path = ElevationConfig.positions_path

if isinstance(ElevationConfig.percent_ranges, str):
    percent_ranges = eval(ElevationConfig.percent_ranges)
    print(f"im string convert to {percent_ranges}")
else:
    percent_ranges = ElevationConfig.percent_ranges
    print("im already string")

positions_bodies = extract_points_from_json(json_file=positions_list_path, payload_flag=ElevationConfig.payload_flag)

reports_path = ElevationConfig.results_path

total_requests = 0
run_number = 1
test_results = []
user_num = 0


class CustomUser(HttpUser):
    wait_time = constant(int(ElevationConfig.wait_time))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = "user"
        self.request_bodies = positions_bodies
        self.request_bodies_cycle = cycle(self.request_bodies)
        self.graph_name = ElevationConfig.graph_name

    @task(1)
    def index(self):
        body = json.loads(next(self.request_bodies_cycle))
        if not ElevationConfig.token_flag:
            self.client.post("/", json=body, headers={'Content-Type': 'application/json'}, verify=False)
        else:
            self.client.post(f"?token={ElevationConfig.TOKEN}", json=body, headers={'Content-Type': 'application/json'})

    def on_stop(self):
        average_response_time = self.environment.runner.stats.total.avg_response_time
        # create_start_time_response_time_graph(graph_name=f"RequestStartTime_vs_ResponseTime-{run_number}",
        #                                       start_time_data=start_time_data, response_time_data=response_time_data)


@events.test_start.add_listener
def on_locust_init(environment, **_kwargs):
    environment.users_count = environment.runner.target_user_count


counters = initiate_counters_by_ranges(config_ranges=percent_ranges)


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters, total_requests

    # if response_time < percent_ranges[0][1]:
    #     counters[f"counter{0}"] += 1
    # elif response_time < percent_ranges[1][1]:
    #     counters[f"counter{1}"] += 1
    # else:
    #     counters[f"counter{2}"] += 1
    for index, range_rsp in enumerate(percent_ranges):
        if range_rsp[1] is None and response_time >= range_rsp[0]:
            counters[f"counter{index + 1}"] += 1
            break
        elif range_rsp[0] <= response_time <= range_rsp[1]:
            counters[f"counter{index + 1}"] += 1
            break

    total_requests += 1


# @events.request.add_listener
# def on_request(response_time, **kwargs):
#     global total_requests, start_time_data
#     start_time = datetime.datetime.fromtimestamp(kwargs['start_time'])
#     response_time_data.append(response_time)
#     start_time_data.append(start_time)
#     total_requests += 1


@events.test_start.add_listener
def reset_data_counters(**kwargs):
    global total_requests, run_number, response_time_data, counters
    total_requests = 0
    run_number += 1
    # start_time_data = []
    # response_time_data = []
    counters = initiate_counters_by_ranges(config_ranges=percent_ranges)


# @events.test_start.add_listener
# def reset_counters(**kwargs):
#     global counters, total_requests
#     counters = counters
#     total_requests = 0

@events.test_stop.add_listener
def on_locust_stop(environment, **kwargs):
    global total_requests, test_results, counters
    average_response_time = environment.runner.stats.total.avg_response_time
    test_results.append({"users": environment.users_count, "avg_response_time": average_response_time})
    create_custom_graph(graph_name="Users_vs_AvgResponseTime", graph_path=reports_path,
                        test_results=test_results, graph_title=None)
    percent_value_by_range = {}
    for index, (key, value) in enumerate(counters.items()):
        percent_range = (value / total_requests) * 100
        percent_value_by_range[f"{percent_ranges[index]}"] = percent_range

    percent_value_by_range["total_requests"] = total_requests
    write_rps_percent_results(
        custom_path=ElevationConfig.results_path, percent_value_by_range=percent_value_by_range
    )
