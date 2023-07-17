from locust import HttpUser, events, task
from matplotlib import pyplot as plt

from common.config.config import ElevationConfig
from common.validation.validation_utils import (
    get_request_parameters,
    initiate_counters_by_ranges,
    read_tests_data_folder,
    write_rps_percent_results,
)

results_path = ElevationConfig.results_path

positions_list_path = ElevationConfig.positions_path

if type(ElevationConfig.percent_ranges) == str:
    percent_ranges = list(ElevationConfig.percent_ranges)
else:
    percent_ranges = ElevationConfig.percent_ranges

request_body = get_request_parameters(positions_list_path=positions_list_path)

request_data_bodies = read_tests_data_folder(
    folder_path=ElevationConfig.bulks_root_folder
)

reports_path = ElevationConfig.results_path


class CustomUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_body = request_body
        self.bulks_amount = len(request_data_bodies)
        self.tasks_per_user = request_data_bodies
        self.test_results = []
        self.users_count = None
        self.graph_name = ElevationConfig.graph_name

    task(1)

    def index(self):
        for file_name, body in self.tasks_per_user.items():
            if "json" in file_name:
                self.client.post(
                    "/", json=body, headers={"Content-Type": "application/json"}
                )
                self.users_count = self.environment.runner.user_count
            elif "bin" in file_name:
                self.client.post(
                    "/",
                    data=body,
                    headers={"Content-Type": "application/octet-stream"},
                )
                self.users_count = self.environment.runner.user_count
            else:
                return "Invalid file type"
                # Process the response as needed

    def on_stop(self):
        average_response_time = self.environment.runner.stats.total.avg_response_time
        self.test_results.append(
            {"users": self.users_count, "avg_response_time": average_response_time}
        )
        self.plot_graph(graph_name=self.graph_name, graph_path=reports_path)
        # Calculate and present the percentage results
        percent_value_by_range = {}
        for index, (key, value) in enumerate(counters.items()):
            percent_range = (value / total_requests) * 100
            percent_value_by_range[f"{percent_ranges[index]}"] = percent_range

        percent_value_by_range["total_requests"] = total_requests
        write_rps_percent_results(
            custom_path=ElevationConfig.results_path,
            percente_value_by_range=percent_value_by_range,
        )

    def plot_graph(self, graph_name, graph_path):
        # Plotting the graph
        users = [result["users"] for result in self.test_results]
        avg_response_times = [
            result["avg_response_time"] for result in self.test_results
        ]

        plt.plot(users, avg_response_times, marker="o")
        plt.ylabel("Average Response Time")
        plt.xlabel("Number of Users")
        plt.title("User amount vs Average Response Time")
        plt.grid(True)
        plt.savefig(f"{graph_path}/{graph_name}.png")
        plt.close()


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
    wait_time = ElevationConfig.wait_time


# todo: config the graph according to bulks amount
