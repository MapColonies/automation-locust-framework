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
total_requests = 0
total_time = 0
avg_requests_per_second = 0


class MyUser(HttpUser):
    wait_time = between(1, 2)
    test_results = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_requests = 0
        self.total_response_time = 0
        self.user_count = None

    @task
    def my_task(self):
        # Make the HTTP request and perform task logic
        self.client.get("https://www.ynet.co.il/home")  # Replace with your actual task logic

        self.user_count = self.environment.runner.user_count

        # Do something with the response if needed
        # response_time = response.elapsed.total_seconds() * 1000

        # self.total_requests += 1
        # self.total_response_time += response_time

    def on_stop(self, **kwargs):
        print(avg_requests_per_second)
        average_response_time = self.environment.runner.stats.total.avg_response_time
        self.test_results.append({"users": self.user_count
                                     , "avg_response_time": average_response_time})
        self.plot_graph()
        print("rps is", self.environment.runner.stats.total.total_rps)

    def plot_graph(self):
        users = [result["users"] for result in self.test_results]
        avg_response_times = [result["avg_response_time"] for result in self.test_results]

        plt.plot(users, avg_response_times, marker='o')
        plt.ylabel('Average Response Time')
        plt.xlabel('Number of Users')
        plt.title("User amount vs Average Response Time")
        plt.grid(True)
        # plt.plot(avg_response_times, users, marker='o')
        # plt.xlabel('Average Response Time (ms)')
        # plt.ylabel('User Count')
        # plt.title('User Count vs. Average Response Time')
        plt.savefig('graph.png')
        plt.close()


@events.request.add_listener
def on_request_success(request_type, name, response_time, response_length, **kwargs):
    global total_requests
    global total_time

    total_requests += 1
    total_time += response_time
    avg_requests_per_second = total_requests / total_time

# @events.quitting.add_listener
# def on_locust_quit(environment, **kwargs):
#     avg_requests_per_second = total_requests / total_time
#     print(f"Average Requests/s: {avg_requests_per_second}")

# @events.quitting.add_listener
# def on_locust_quit(environment, **kwargs):
#     total_users = environment.runner.user_count
#     print(f"Total users at the end of the test: {total_users}")
