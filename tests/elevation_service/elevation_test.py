import json

from locust import HttpUser, events, task

from common.config.config import ElevationConfig
from common.validation.validation_utils import (
    extract_file_type,
    write_rps_percent_results, get_request_body_parameters, create_ranges_counters
)

positions_list_path = ElevationConfig.positions_path
results_path = ElevationConfig.results_path

request_body = get_request_body_parameters(positions_list_path)

percent_ranges = ElevationConfig.percent_ranges

ranges_counters = create_ranges_counters(ranges_list=percent_ranges)


class CustomUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_body = request_body

    # def on_start(self):
    #     request_type = extract_file_type(file_path=positions_list_path)
    #     if request_type == "json":
    #         with open(positions_list_path) as file:
    #             body = json.load(file)
    #             self.request_body = {"request_type": request_type, "body": body,
    #                                  "header": {"Content-Type": "application/json"}}
    #     elif request_type == "bin":
    #         with open(positions_list_path, "rb") as file:
    #             body = file.read()
    #             self.request_body = {"request_type": request_type, "body": body,
    #                                  "header": {'Content-Type': 'application/octet-stream'}}
    #     else:
    #         return "invalid file path"

    @task(1)
    def index(self):
        if self.request_body["request_type"] == "json":
            self.client.post(
                "/", json=self.request_body["body"], headers=self.request_body["header"],
                verify=True
            )
        elif self.request_body["request_type"] == "bin":
            print("hello from bin-post")
            self.client.post(
                "/",
                data=self.request_body["body"],
                headers=self.request_body["header"],
                verify=True,
            )
        # Process the response as needed

    def on_stop(self):
        percent_value_by_range = {}
        for k, v in ranges_counters:
            percent_range = (v / total_requests) * 100
            percent_value_by_range[k] = percent_range
        write_rps_percent_results(
            custom_path=results_path, percente_value_by_range=percent_value_by_range
        )

    # def on_stop(self):
    #     # Calculate and present the percentage results
    #     percent_range_1 = (counter_range_1 / total_requests) * 100
    #     percent_range_2 = (counter_range_2 / total_requests) * 100
    #     percent_range_3 = (counter_range_3 / total_requests) * 100
    #
    #     percent_value_by_range = {
    #         f"{range_1}": f"{percent_range_1}%",
    #         f"{range_2}": f"{percent_range_2}%",
    #         f"{range_3}": f"{percent_range_3}%",
    #         "total_requests": f"{total_requests}",
    #     }
    #     write_rps_percent_results(
    #         custom_path=results_path, percente_value_by_range=percent_value_by_range
    #     )


# Define the response time counters
# counter_range_1 = 0
# counter_range_2 = 0
# counter_range_3 = 0

total_requests = 0


#
# # Define the response time ranges
# range_1 = (0, 100)
# range_2 = (101, 500)
# range_3 = (501, None)

@events.request.add_listener
def response_time_listener(response_time, ranges_counters, **kwargs):
    # global counter_range_1, counter_range_2, counter_range_3, total_requests
    global total_requests
    for key, val in ranges_counters:
        if key[1] is None:
            if response_time >= key[0]:
                val += 1
                ranges_counters[key] = val
        if key[0] <= response_time <= key[1]:
            val += 1
            ranges_counters[key] = val
    total_requests += 1


# Define the response time event hook
# @events.request.add_listener
# def response_time_listener(response_time, **kwargs):
#     global counter_range_1, counter_range_2, counter_range_3, total_requests
#
#     if range_1[0] <= response_time <= range_1[1]:
#         counter_range_1 += 1
#     elif range_2[0] <= response_time <= range_2[1]:
#         counter_range_2 += 1
#     elif response_time >= range_3[0]:
#         counter_range_3 += 1
#
#     total_requests += 1


# @events.test_start.add_listener
# def reset_counters(**kwargs):
#     global counter_range_1, counter_range_2, counter_range_3, total_requests
#
#     counter_range_1 = 0
#     counter_range_2 = 0
#     counter_range_3 = 0
#     total_requests = 0

# @events.test_start.add_listener
# def reset_counters(ranges_counters=ranges_counters, **kwargs):
#     for key, val in ranges_counters:
#         ranges_counters[key] = 0
#     total_requests = 0


# Run the Locust test
class MyUser(CustomUser):
    min_wait = 100
    max_wait = 1000
