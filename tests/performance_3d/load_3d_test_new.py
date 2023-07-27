from locust import HttpUser, events, task
from locust_plugins.csvreader import CSVReader

from common.config.config import config_obj
from common.utils.constants.TimerStrings import TimerStrings
from common.validation.validation_utils import write_rps_percent_results

ssn_reader = CSVReader(config_obj["_3d"].CSV_DATA_PATH)
results_path = config_obj["_3d"].RESULTS_PATH


class ResponseTimeRanges:
    RANGE_1 = (0, 100)
    RANGE_2 = (101, 500)
    RANGE_3 = (501, None)


class ResponseTimeCounter:
    def __init__(self):
        self.reset_counters()

    def reset_counters(self):
        self.counter_range_1 = 0
        self.counter_range_2 = 0
        self.counter_range_3 = 0
        self.total_requests = 0

    def update_counters(self, response_time):
        if (
            ResponseTimeRanges.RANGE_1[0]
            <= response_time
            <= ResponseTimeRanges.RANGE_1[1]
        ):
            self.counter_range_1 += 1
        elif (
            ResponseTimeRanges.RANGE_2[0]
            <= response_time
            <= ResponseTimeRanges.RANGE_2[1]
        ):
            self.counter_range_2 += 1
        elif response_time >= ResponseTimeRanges.RANGE_3[0]:
            self.counter_range_3 += 1
        self.total_requests += 1

    def get_percentage_results(self):
        percent_range_1 = (self.counter_range_1 / self.total_requests) * 100
        percent_range_2 = (self.counter_range_2 / self.total_requests) * 100
        percent_range_3 = (self.counter_range_3 / self.total_requests) * 100
        return {
            f"{ResponseTimeRanges.RANGE_1}": f"{percent_range_1}%",
            f"{ResponseTimeRanges.RANGE_2}": f"{percent_range_2}%",
            f"{ResponseTimeRanges.RANGE_3}": f"{percent_range_3}%",
            "total_requests": f"{self.total_requests}",
        }


counter = ResponseTimeCounter()


class User(HttpUser):
    timer_selection = config_obj["wmts"].WAIT_TIME_FUNC
    wait_time_config = config_obj["wmts"].WAIT_TIME
    wait_time, timer_message = TimerStrings.set_wait_time(
        timer_selection, wait_time_config
    )
    print(timer_message)

    @task(1)
    def index(self):
        url = next(ssn_reader)
        self.client.get(url=url[1], verify=False)

    host = config_obj["default"].HOST

    def on_stop(self):
        percent_value_by_range = counter.get_percentage_results()
        write_rps_percent_results(
            custome_path=results_path, percente_value_by_range=percent_value_by_range
        )


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    counter.update_counters(response_time)


@events.test_start.add_listener
def reset_counters(**kwargs):
    counter.reset_counters()
