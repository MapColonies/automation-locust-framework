import random

from locust import HttpUser, constant, events, task, constant_pacing, between, constant_throughput

from common.config.config import ElevationConfig, config_obj
from common.utils.constants.strings import INVALID_TIMER_STR, CONSTANT_PACING_TIMER_STR, BETWEEN_TIMER_STR, \
    CONSTANT_THROUGHPUT_TIMER_STR, CONSTANT_TIMER_STR
from common.utils.data_generator.data_utils import generate_points_request
from common.validation.validation_utils import (
    find_range_for_response_time,
    initiate_counters_by_ranges,
    retype_env,
    write_rps_percent_results,
)

if isinstance(ElevationConfig.percent_ranges, str):
    percent_ranges = retype_env(ElevationConfig.percent_ranges)
    percent_ranges.append(0)
    percent_ranges.append(float("inf"))
    percent_ranges = sorted(percent_ranges)
else:
    percent_ranges = ElevationConfig.percent_ranges
    percent_ranges.append(0)
    percent_ranges.append(float("inf"))
    percent_ranges = sorted(percent_ranges)

reports_path = ElevationConfig.results_path

if isinstance(ElevationConfig.poly, str):
    polygons = retype_env(ElevationConfig.poly)
else:
    polygons = ElevationConfig.poly
if isinstance(ElevationConfig.wait_time, str):
    wait_time = retype_env(ElevationConfig.wait_time)
else:
    wait_time = ElevationConfig.wait_time

if isinstance(ElevationConfig.exclude_fields, str):
    exclude_fields = retype_env(ElevationConfig.exclude_fields)
else:
    exclude_fields = ElevationConfig.exclude_fields

def set_wait_time(timer_selection, wait_time):
    if timer_selection == 1:
        return constant(wait_time), CONSTANT_TIMER_STR
    elif timer_selection == 2:
        return constant_throughput(wait_time), CONSTANT_THROUGHPUT_TIMER_STR
    elif timer_selection == 3:
        return between(wait_time["min_wait"], wait_time["max_wait"]), BETWEEN_TIMER_STR
    elif timer_selection == 4:
        return constant_pacing(wait_time), CONSTANT_PACING_TIMER_STR
    else:
        return None, INVALID_TIMER_STR
class CustomUser(HttpUser):
    response_times = []
    timer_selection = config_obj["wmts"].WAIT_TIME_FUNC
    wait_time_config = config_obj["wmts"].WAIT_TIME
    wait_time, timer_message = set_wait_time(timer_selection, wait_time_config)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.avg_response_time = None
        self.points_amount_range = ElevationConfig.points_amount_range
        self.points_amount = random.randint(0, self.points_amount_range)
        self.poly = random.choice(polygons)

    @task(1)
    def index(self):
        body = generate_points_request(
            points_amount=self.points_amount,
            polygon=self.poly,
            exclude_fields=exclude_fields,
        )
        print("-----------", body, "-----------")
        if retype_env(ElevationConfig.token_flag):
            self.client.post(
                f"?token={ElevationConfig.TOKEN}",
                data=body,
                headers={"Content-Type": "application/json"},
            )
        else:
            self.client.post(
                "/",
                data=body,
                headers={"Content-Type": "application/json"},
                verify=False,
            )


# create counters for each range value from the configuration
counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
total_requests = 0
test_results = []
response_time_data = []
points_amount_avg_rsp = []
avg_response_time = 0


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters, total_requests
    counters = find_range_for_response_time(
        response_time=response_time, ranges_list=percent_ranges, counters_dict=counters
    )
    total_requests += 1


@events.test_start.add_listener
def reset_counters(**kwargs):
    global counters, total_requests, response_time_data
    counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
    total_requests = 0
    response_time_data = []


@events.test_stop.add_listener
def on_locust_stop(environment, **kwargs):
    """
    The percent calculation for each range by range counters
    after calculate the percent value with the result into json file
    :return:
    """

    global total_requests, counters
    percent_value_by_range = {}
    print(counters)
    if total_requests != 0:
        for index, (key, value) in enumerate(counters.items()):
            percent_range = (value / total_requests) * 100
            percent_value_by_range[f"{key}"] = percent_range

        percent_value_by_range["total_requests"] = int(total_requests)
        write_rps_percent_results(
            custom_path=ElevationConfig.results_path,
            percent_value_by_range=percent_value_by_range,
        )

    else:
        print(
            "The test execution failed - requests did not proceed. Check the logs to find the problem"
        )


# Run the Locust test
# class MyUser(CustomUser):
#     wait_time = constant(int(ElevationConfig.wait_time))
