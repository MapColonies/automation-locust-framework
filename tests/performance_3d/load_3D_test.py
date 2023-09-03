from locust import (
    HttpUser,
    between,
    constant,
    constant_pacing,
    constant_throughput,
    events,
    task,
)

from common.config.config import Config, config_obj
from common.utils.constants.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)
from common.utils.csvreader import CSVReader
from common.validation.validation_utils import (
    find_range_for_response_time,
    initiate_counters_by_ranges,
    write_rps_percent_results,
)
from playgorund.create_ranges_counter import initiate_counters_by_ranges

ssn_reader = CSVReader(config_obj["_3d"].CSV_DATA_PATH)
results_path = config_obj["_3d"].RESULTS_PATH


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


class User(HttpUser):
    timer_selection = config_obj["wmts"].WAIT_TIME_FUNC
    wait_time_config = config_obj["wmts"].WAIT_TIME
    wait_time, timer_message = set_wait_time(timer_selection, wait_time_config)
    print(timer_message)

    @task(1)
    def index(self):
        url = next(ssn_reader)
        self.client.get(url=url[1], verify=False)

    host = config_obj["default"].HOST


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
            custom_path=Config.RESULTS_PATH,
            percent_value_by_range=percent_value_by_range,
        )
    else:
        print(
            "The test execution failed - requests did not proceed. Check the logs to find the problem"
        )


# Define the response time counters
counter_range_1 = 0
counter_range_2 = 0
counter_range_3 = 0
total_requests = 0

# Define the response time ranges
range_1 = (0, 100)
range_2 = (101, 500)
range_3 = (501, None)


# Define the response time event hook
@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counter_range_1, counter_range_2, counter_range_3, total_requests

    if range_1[0] <= response_time <= range_1[1]:
        counter_range_1 += 1
    elif range_2[0] <= response_time <= range_2[1]:
        counter_range_2 += 1
    elif response_time >= range_3[0]:
        counter_range_3 += 1

    total_requests += 1


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters, total_requests
    counters = find_range_for_response_time(
        response_time=response_time, ranges_list=percent_ranges, counters_dict=counters
    )
    total_requests += 1


@events.test_start.add_listener
def reset_counters(**kwargs):
    global counters, total_requests, run_number, start_time_data, response_time_data
    counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
    total_requests = 0
    run_number += 1
    start_time_data = []
    response_time_data = []


# todo: add all percent dependencies for the percent calculation and add configurations
