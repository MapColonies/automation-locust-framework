import time
from itertools import cycle

from locust import HttpUser, constant, events, task
from matplotlib import pyplot as plt

from common.config.config import ElevationConfig
from common.validation.validation_utils import (
    extract_points_from_json,
    initiate_counters_by_ranges,
)

positions_list_path = ElevationConfig.positions_path

if type(ElevationConfig.percent_ranges) == str:
    percent_ranges = list(ElevationConfig.percent_ranges)
else:
    percent_ranges = ElevationConfig.percent_ranges

positions_bodies = extract_points_from_json(json_file=positions_list_path)


class CustomUser(HttpUser):
    # self.test_start_time = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_results = []
        self.request_bodies = positions_bodies
        self.request_bodies_cycle = cycle(self.request_bodies)
        self.test_start_time = time.time()
        self.average_response_time = 0
        self.total_requests = 0
        self.total_response_time = 0
        self.total_users = 0

    @task(1)
    def index(self):
        # num_users = self.environment.runner.user_count
        # print(f"Number of users: {num_users}")
        # body = next(self.request_bodies_cycle)
        # self.body = json.loads(body)
        # if self.request_bodies["request_type"] == "json":
        response = self.client.get("https://www.ynet.co.il/home")
        response_time = response.elapsed.total_seconds() * 1000
        self.total_requests += 1
        self.total_response_time += response_time
        # elif self.request_bodies["request_type"] == "bin":
        #     self.client.post(
        #         "/",
        #         data=self.request_bodies["body"],
        #         headers=self.request_bodies["header"],
        #     )

        # Process the response as needed

    def on_stop(self):
        self.total_users = self.environment.runner.user_count

        # Calculate the test duration
        if self.total_requests > 0:
            self.average_response_time = self.total_response_time / self.total_requests
        else:
            self.average_response_time = 0

        # Store the data in the test_results list
        self.test_results.append(
            {"users": self.total_users, "rps": self.average_response_time}
        )

        # Plot the graph after the final test execution
        # if self.environment.runner.user_count == 0:
        self.plot_graph()
        # percent_value_by_range = {}
        # if total_requests != 0:
        #     for index, (key, value) in enumerate(counters.items()):
        #         percent_range = (value / total_requests) * 100
        #         percent_value_by_range[f"{percent_ranges[index]}"] = percent_range
        #     percent_value_by_range["total_requests"] = total_requests
        #     write_rps_percent_results(
        #         custom_path=ElevationConfig.results_path, percente_value_by_range=percent_value_by_range
        #     )
        # else:
        #     percent_value_by_range["total_requests"] = total_requests

    def plot_graph(self):
        users = [result["users"] for result in self.test_results]
        rps = [result["rps"] for result in self.test_results]

        # Plotting the graph
        plt.plot(users, rps, marker="o")
        plt.xlabel("Number of Users")
        plt.ylabel("Average Total Requests")
        plt.title("Test Set: Users vs Average Total Requests")
        plt.grid(True)
        plt.savefig("graph.png")
        # plt.show()


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
