import json
from locust import HttpUser, events, task, constant
from itertools import cycle
from matplotlib import pyplot as plt
from common.config.config import ElevationConfig
from common.validation.validation_utils import (
    write_rps_percent_results, extract_points_from_json, initiate_counters_by_ranges,
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

    @task(1)
    def index(self):
        body = json.loads(next(self.request_bodies_cycle))
        # if self.request_bodies["request_type"] == "json":
        self.client.post("/", json=body, headers={'Content-Type': 'application/json'}, verify=False)
        # elif self.request_bodies["request_type"] == "bin":
        #     self.client.post(
        #         "/",
        #         data=self.request_bodies["body"],
        #         headers=self.request_bodies["header"],
        #     )
        self.users_count = self.environment.runner.user_count

    def on_stop(self):
        average_response_time = self.environment.runner.stats.total.avg_response_time
        self.test_results.append({"users": self.users_count, "avg_response_time": average_response_time})
        self.plot_graph(graph_name=self.graph_name, graph_path=reports_path)

        percent_value_by_range = {}
        if total_requests != 0:
            for index, (key, value) in enumerate(counters.items()):
                percent_range = (value / total_requests) * 100
                percent_value_by_range[f"{percent_ranges[index]}"] = percent_range
            percent_value_by_range["total_requests"] = total_requests
            write_rps_percent_results(
                custom_path=reports_path, percente_value_by_range=percent_value_by_range
            )
        else:
            percent_value_by_range["total_requests"] = total_requests

    def plot_graph(self, graph_name, graph_path):
        # Plotting the graph
        users = [result["users"] for result in self.test_results]
        avg_response_times = [result["avg_response_time"] for result in self.test_results]

        plt.plot(users, avg_response_times, marker='o')
        plt.ylabel('Average Response Time')
        plt.xlabel('Number of Users')
        plt.title("User amount vs Average Response Time")
        plt.grid(True)
        plt.savefig(f'{graph_path}/{graph_name}.png')


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
    wait_time = constant(ElevationConfig.wait_time)
