from locust import HttpUser, events, task, constant
from common.config.config import ElevationConfig
from common.validation.validation_utils import (
    write_rps_percent_results, get_request_parameters, read_tests_data_folder, initiate_counters_by_ranges,
    create_custom_graph, get_bulks_points_amount, calculate_response_time_percent,
)

results_path = ElevationConfig.results_path

positions_list_path = ElevationConfig.positions_path

if type(ElevationConfig.percent_ranges) == str:
    percent_ranges = list(ElevationConfig.percent_ranges)
else:
    percent_ranges = ElevationConfig.percent_ranges

request_body = get_request_parameters(positions_list_path=positions_list_path)

request_data_bodies = read_tests_data_folder(folder_path=ElevationConfig.bulks_root_folder)

reports_path = ElevationConfig.results_path

points_amount = get_bulks_points_amount(bulk_content=next(iter(request_data_bodies.values())))
bulks_amount = len(request_data_bodies)


class CustomUser(HttpUser):
    response_times = []
    avg_response_time = None
    wait_time = constant(int(ElevationConfig.wait_time))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_body = request_body

        self.tasks_per_user = request_data_bodies
        self.users_count = None
        self.graph_name = ElevationConfig.graph_name
        self.avg_response_time = None

    @task(1)
    def index(self):
        if not ElevationConfig.token_flag:
            for bulk_name, body in self.tasks_per_user.items():
                if "json" in bulk_name:
                    self.client.post(
                        "/", json=body, headers={"Content-Type": "application/json"}, verify=False)
                    # self.log_response_time(response.elapsed.total_seconds() * 1000)

                elif "bin" in bulk_name:
                    self.client.post(
                        "/",
                        data=body,
                        headers={"Content-Type": "application/octet-stream"},
                    )
                    self.users_count = self.environment.runner.user_count
                else:
                    return "Invalid file type"
                    # Process the response as needed
        else:
            for bulk_name, body in self.tasks_per_user.items():
                if "json" in bulk_name:
                    self.client.post(
                        f"?token={ElevationConfig.TOKEN}", json=body, headers={"Content-Type": "application/json"}
                    )
                    self.users_count = self.environment.runner.user_count
                    # self.log_response_time(response.elapsed.total_seconds() * 1000)

                elif "bin" in bulk_name:
                    self.client.post(
                        f"?token={ElevationConfig.TOKEN}",
                        data=body,
                        headers={"Content-Type": "application/octet-stream"},
                    )
                    self.users_count = self.environment.runner.user_count
                else:
                    return "Invalid file type"
                    # Process the response as needed


file_created = False
counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
total_requests = 0
test_results = []
response_time_data = []
points_amount_avg_rsp = []
avg_response_time = 0


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
    global counters, total_requests, response_time_data
    counters = counters
    total_requests = 0
    response_time_data = []


@events.request.add_listener
def on_request(response_time, **kwargs):
    response_time_data.append(response_time)


@events.test_stop.add_listener
def on_locust_stop(environment, **kwargs):
    # global test_results
    avg_response_time = environment.runner.stats.total.avg_response_time
    test_results.append({"bulks_amount": bulks_amount, "avg_response_time": avg_response_time})
    points_amount_avg_rsp.append({"points_amount": points_amount, "avg_response_time": avg_response_time})
    create_custom_graph(graph_name="PointsVsAvgResponseTime", graph_title="Points amount VS Avg response time",
                        graph_path=reports_path, test_results=points_amount_avg_rsp)
    create_custom_graph(graph_name="BulkAmountVsAvgResponseTime", graph_title="Bulk amount VS Avg response time",
                        graph_path=reports_path, test_results=test_results)

    percent_value_by_ranges = calculate_response_time_percent(response_times=response_time_data,
                                                              range_values=percent_ranges)
    percent_value_by_ranges["total_requests"] = total_requests
    write_rps_percent_results(
        custom_path=reports_path, percent_value_by_range=percent_value_by_ranges
    )

# Run the Locust test
