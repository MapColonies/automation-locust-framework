import time

from locust import task, events, HttpUser, between
import matplotlib.pyplot as plt

import gevent
from locust import events
from locust.runners import STATE_STOPPED, STATE_CLEANUP, MasterRunner, LocalRunner, STATE_STOPPING


# def print_current_users(environment):
#     while not environment.runner.state in [STATE_STOPPED, STATE_CLEANUP]:
#         time.sleep(2)
#         print(f"Currently running users: {environment.runner.user_count}")
#
# @events.init.add_listener
# def on_locust_init(environment, **_kwargs):
#     # don't run this on workers, we only care about the aggregated numbers
#     if isinstance(environment.runner, MasterRunner) or isinstance(environment.runner, LocalRunner):
#         gevent.spawn(print_current_users, environment)


# Print the last user count after the test execution


class MyUser(HttpUser):
    wait_time = between(1, 2)
    test_results = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_requests = 0
        self.total_response_time = 0

    @task
    def my_task(self):
        # Make the HTTP request and perform task logic
        response = self.client.get("https://www.ynet.co.il/home")  # Replace with your actual task logic

        # Do something with the response if needed
        response_time = response.elapsed.total_seconds() * 1000

        self.total_requests += 1
        self.total_response_time += response_time

    def on_stop(self, **kwargs):
        if self.environment.runner.stats in [STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP]:
            user_count = self.environment.runner.user_count

            print("users------------>", user_count)
        else:
            user_count = self.environment.runner.user_count

            print("users------------>", user_count)
        average_response_time = self.environment.runner.stats.total.avg_response_time
        # print("average_response_time is", average_response_time)
        # self.test_results.append({"users": users
        #                              , "avg_response_time": average_response_time})
        # self.plot_graph()

    def plot_graph(self):
        users = [result["users"] for result in self.test_results]
        avg_response_times = [result["avg_response_time"] for result in self.test_results]

        plt.plot(users, avg_response_times, marker='o')
        plt.xlabel('Number of Users')
        plt.ylabel('Average Response Time (ms)')
        plt.title('Test Set: Users vs Average Response Time')
        plt.grid(True)
        plt.savefig('graph.png')


