import json
import os
from collections import defaultdict

from locust import HttpUser, task, between
import matplotlib.pyplot as plt

from build.lib.common.validation.validation_utils import create_custom_graph


class MyUser(HttpUser):
    wait_time = between(1, 2)  # Adjust the wait time between requests
    response_times = defaultdict(list)
    request_bodies = [
        "https://www.ynet.co.il/home", "https://www.ynet.co.il/food"
    ]

    @task
    def my_task(self):
        for payload in self.request_bodies:
            response = self.client.get(url=payload)

            self.log_request_data(payload)
            self.log_response_time(payload,
                                   response.elapsed.total_seconds() * 1000)  # Log the response time in milliseconds

    def on_stop(self):
        bulks_rsp_time_results = []
        for payload, response_times in self.response_times.items():
            avg_response_time = sum(response_times) / len(response_times)
            print(f"Average response time for {payload}: {avg_response_time} ms")
            bulks_rsp_time_results.append({"bulk_name": payload, "avg_response_time": avg_response_time})
            print(bulks_rsp_time_results)
        create_custom_graph(graph_name="check", graph_path=os.getcwd(), test_results=bulks_rsp_time_results,
                            graph_title=None)

    def log_request_data(self, payload):
        print("Request Payload:", payload)

    def log_response_time(self, payload, response_time):
        self.response_times[payload].append(response_time)
        print(self.response_times)
