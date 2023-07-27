import datetime
from itertools import cycle

from locust import HttpUser, constant, events, task

from common.config.config import ElevationConfig
from common.validation.validation_utils import (
    calculate_response_time_percent,
    create_custom_graph,
    create_start_time_response_time_graph,
    extract_points_from_json,
    write_rps_percent_results,
)

positions_list_path = ElevationConfig.positions_path

if type(ElevationConfig.percent_ranges) == str:
    percent_ranges = list(ElevationConfig.percent_ranges)
else:
    percent_ranges = ElevationConfig.percent_ranges

positions_bodies = extract_points_from_json(
    json_file=positions_list_path, payload_flag=ElevationConfig.payload_flag
)

reports_path = ElevationConfig.results_path


class CustomUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_bodies = positions_bodies
        self.request_bodies_cycle = cycle(self.request_bodies)
        self.graph_name = ElevationConfig.graph_name

    @task(1)
    def index(self):
        # body = json.loads(next(self.request_bodies_cycle))
        # if self.request_bodies["request_type"] == "json":
        self.client.get(url="https://www.ynet.co.il/home")
        # elif self.request_bodies["request_type"] == "bin":
        #     self.client.post(
        #         "/",
        #         data=self.request_bodies["body"],
        #         headers=self.request_bodies["header"],
        #     )

    def on_stop(self):
        # average_response_time = self.environment.runner.stats.total.avg_response_time
        # self.test_results.append({"users": self.users_count, "avg_response_time": average_response_time})
        # print(self.test_results)
        # create_custom_graph(graph_name="Users_vs_AvgResponseTime", graph_path=reports_path,
        #                     test_results=self.test_results, graph_title=None)

        # self.req_start_t_rsp_t = create_graph_results_data_format(["start_time", "response_time"],
        #                                                           [])
        # print(self.req_start_t_rsp_t)
        create_start_time_response_time_graph(
            graph_name=f"RequestStartTime_vs_ResponseTime-{run_number}",
            start_time_data=start_time_data,
            response_time_data=response_time_data,
        )


# counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
total_requests = 0
run_number = 1
start_time_data = []
response_time_data = []
users_count = 0
test_results = []


@events.request.add_listener
def on_request(environment, request_type, name, response_time, **kwargs):
    global total_requests, users_count
    start_time = datetime.datetime.fromtimestamp(kwargs["start_time"])
    response_time_data.append(response_time)
    start_time_data.append(start_time)
    total_requests += 1
    users_count = environment.runner.user_count


@events.test_start.add_listener
def reset_counters(environment, **kwargs):
    global counters, total_requests, run_number, start_time_data, response_time_data
    counters = counters
    total_requests = 0
    run_number += 1
    start_time_data = []
    response_time_data = []


@events.test_stop.add_listener
def on_locust_stop(environment, **kwargs):
    print("users_count is:", users_count)
    print("response_time_data is:", response_time_data)
    average_response_time = environment.runner.stats.total.avg_response_time
    test_results.append(
        {"users": users_count, "avg_response_time": average_response_time}
    )
    print(test_results)
    create_custom_graph(
        graph_name="Users_vs_AvgResponseTime",
        graph_path=reports_path,
        test_results=test_results,
        graph_title=None,
    )
    percent_value_by_ranges = calculate_response_time_percent(
        response_times=response_time_data, range_values=percent_ranges
    )
    percent_value_by_ranges["total_requests"] = total_requests
    write_rps_percent_results(
        custom_path=reports_path, percent_value_by_range=percent_value_by_ranges
    )


# Run the Locust test
class MyUser(CustomUser):
    wait_time = constant(int(ElevationConfig.wait_time))
