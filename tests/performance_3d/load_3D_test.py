from locust import (
    HttpUser,
    between,
    constant,
    constant_pacing,
    constant_throughput,
    events,
    task,
)
from common.utils.csvreader import CSVReader

from common.config.config import config_obj
from common.utils.constants.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)
from common.validation.validation_utils import write_rps_percent_results

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

    def on_stop(self):
        # Calculate and present the percentage results
        percent_range_1 = (counter_range_1 / total_requests) * 100
        percent_range_2 = (counter_range_2 / total_requests) * 100
        percent_range_3 = (counter_range_3 / total_requests) * 100

        percent_value_by_range = {
            f"{range_1}": f"{percent_range_1}%",
            f"{range_2}": f"{percent_range_2}%",
            f"{range_3}": f"{percent_range_3}%",
            "total_requests": f"{total_requests}",
        }
        write_rps_percent_results(
            custom_path=results_path, percente_value_by_range=percent_value_by_range
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


@events.test_start.add_listener
def reset_counters(**kwargs):
    global counter_range_1, counter_range_2, counter_range_3, total_requests

    counter_range_1 = 0
    counter_range_2 = 0
    counter_range_3 = 0
    total_requests = 0
