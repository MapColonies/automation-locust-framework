from locust import HttpUser, events, task, constant
from common.config.config import ElevationConfig
from common.validation.validation_utils import (
    write_rps_percent_results, get_request_parameters, read_tests_data_folder, initiate_counters_by_ranges,
    create_custom_graph, get_bulks_points_amount, retype_env,
)

results_path = ElevationConfig.results_path

positions_list_path = ElevationConfig.positions_path

if isinstance(ElevationConfig.percent_ranges, str):
    percent_ranges = retype_env(ElevationConfig.percent_ranges)
else:
    percent_ranges = ElevationConfig.percent_ranges


request_body = get_request_parameters(positions_list_path=positions_list_path)

request_data_bodies = read_tests_data_folder(folder_path=ElevationConfig.bulks_root_folder)
print(request_data_bodies)
reports_path = ElevationConfig.results_path

points_amount = get_bulks_points_amount(bulk_content=next(iter(request_data_bodies.values())))
print(points_amount)
bulks_amount = len(request_data_bodies)

ranges = [tup[1] for tup in percent_ranges]


class CustomUser(HttpUser):
    response_times = []
    wait_time = constant(int(ElevationConfig.wait_time))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_body = request_body
        self.tasks_per_user = request_data_bodies
        self.graph_name = ElevationConfig.graph_name
        self.avg_response_time = None

    @task(1)
    def index(self):
        if not retype_env(ElevationConfig.token_flag):
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
                else:
                    return "Invalid file type"
                    # Process the response as needed
        else:
            for bulk_name, body in self.tasks_per_user.items():
                if "json" in bulk_name:
                    self.client.post(
                        f"?token={ElevationConfig.TOKEN}", json=body, headers={"Content-Type": "application/json"}
                    )
                    # self.log_response_time(response.elapsed.total_seconds() * 1000)

                elif "bin" in bulk_name:
                    self.client.post(
                        f"?token={ElevationConfig.TOKEN}",
                        data=body,
                        headers={"Content-Type": "application/octet-stream"},
                    )
                else:
                    return "Invalid file type"
                    # Process the response as needed


counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
total_requests = 0
test_results = []
response_time_data = []
points_amount_avg_rsp = []
avg_response_time = 0


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters, total_requests
    #
    # for index, range_val in enumerate(percent_ranges):
    #     if range_val[1] is None and response_time >= range_val[0]:
    #         counters[f"counter{index + 1}"] += 1
    #         break
    #     elif range_val[0] <= response_time <= range_val[1]:
    #         counters[f"counter{index + 1}"] += 1
    #         break
    # total_requests += 1
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


# @events.test_start.add_listener
# def on_locust_init(environment, **_kwargs):
#     environment.users_count = environment.runner.target_user_count


@events.test_stop.add_listener
def on_locust_stop(environment, **kwargs):
    global total_requests, counters
    avg_response_time = environment.runner.stats.total.avg_response_time
    test_results.append({"bulks_amount": bulks_amount, "avg_response_time": avg_response_time})
    points_amount_avg_rsp.append({"points_amount": points_amount, "avg_response_time": avg_response_time})
    create_custom_graph(graph_name="PointsVsAvgResponseTime", graph_title="Points amount VS Avg response time",
                        graph_path=reports_path, test_results=points_amount_avg_rsp)
    create_custom_graph(graph_name="BulkAmountVsAvgResponseTime", graph_title="Bulk amount VS Avg response time",
                        graph_path=reports_path, test_results=test_results)

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
