import datetime
import logging
import random

from locust import HttpUser, constant, events, task

from common.config.config import ElevationConfig
from common.utils.data_generator.data_utils import generate_points_request
from common.validation.validation_utils import (
    find_range_for_response_time,
    initiate_counters_by_ranges,
    parse_response_content,
    retype_env,
    write_rps_percent_results,
)

reports_path = ElevationConfig.results_path

now = datetime.datetime.now()
current_date = now.strftime("%Y-%m-%d")
logger = logging.getLogger("elevation_logger")

logger.setLevel(logging.INFO)

log_file = f"{reports_path}/{current_date}"
file_handler = logging.FileHandler(log_file)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

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

# ranges = [tup[1] for tup in percent_ranges]

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


class CustomUser(HttpUser):
    response_times = []
    wait_time = constant(wait_time)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.avg_response_time = None
        self.poly = random.choice(polygons)
        # print(self.poly)

    @task(1)
    def index(self):
        body = generate_points_request(
            points_amount=ElevationConfig.points_amount_range,
            polygon=self.poly,
            exclude_fields=exclude_fields,
        )
        if retype_env(ElevationConfig.token_flag):
            response = self.client.post(
                f"?token={ElevationConfig.TOKEN}",
                data=body,
                headers={"Content-Type": "application/json"},
            )
            response_time = response.elapsed.total_seconds() * 1000
            log = parse_response_content(
                response_content=response.json(),
                response_time=response_time,
                normality_threshold=ElevationConfig.normality_threshold,
                property_name="height",
            )
            if log:
                logger.error(log)

        else:
            response = self.client.post(
                "/",
                data=body,
                headers={"Content-Type": "application/json"},
                verify=False,
            )
            response_time = response.elapsed.total_seconds() * 1000
            log = parse_response_content(
                response_content=response.json(),
                response_time=response_time,
                normality_threshold=ElevationConfig.normality_threshold,
                property_name="height",
            )
            if log:
                logger.error(log)


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
    global counters, total_requests, run_number, start_time_data, response_time_data
    counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
    total_requests = 0
    start_time_data = []
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
