import random

from locust import HttpUser, constant, events, task, constant_pacing, between, constant_throughput

from common.config.config import ElevationConfig, config_obj
from common.utils.constants.strings import INVALID_TIMER_STR, CONSTANT_PACING_TIMER_STR, BETWEEN_TIMER_STR, \
    CONSTANT_THROUGHPUT_TIMER_STR, CONSTANT_TIMER_STR
from common.utils.data_generator.data_utils import generate_points_request, custom_sorting_key
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

stats = {"total_requests": 0}
counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
print(counters)
counters_keys = list(counters.keys())


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
            response = self.client.post(
                f"?token={ElevationConfig.TOKEN}",
                data=body,
                headers={"Content-Type": "application/json"},
            )
            if ('content-type', "application/json") not in response.headers.items():
                print(f"invalid response content type for url: {body}")


        else:
            response = self.client.post(
                "/",
                data=body,
                headers={"Content-Type": "application/json"},
                verify=False,
            )


# create counters for each range value from the configuration


@events.init.add_listener
def locust_init(environment, **kwargs):
    """
    We need somewhere to store the stats.
    On the master node stats will contain the aggregated sum of all content-lengths,
    while on the worker nodes this will be the sum of the content-lengths since the
    last stats report was sent to the master
    """
    if environment.web_ui:
        # this code is only run on the master node (the web_ui instance doesn't exist on workers)
        @environment.web_ui.app.route("/total_requests")
        def total_content_length():
            """
            Add a route to the Locust web app, where we can see the total content-length
            """
            requests_amount = stats["total_requests"]
            percent_value_by_range = {}
            print(counters)

            if requests_amount != 0:
                for index, (key, value) in enumerate(counters.items()):
                    percent_range = (value / requests_amount) * 100
                    percent_value_by_range[f"{key}"] = percent_range

                # percent_value_by_range["total_requests"] = int(requests_amount)
                # print(percent_value_by_range)
                percent_value_by_range = dict(sorted(percent_value_by_range.items(), key=custom_sorting_key))
            return {"percent_value": percent_value_by_range,
                    "total_requests": stats["total_requests"]}


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters
    print("percent_ranges is", percent_ranges)
    counters = find_range_for_response_time(
        response_time=response_time, ranges_list=percent_ranges, counters_dict=counters
    )
    # total_requests += 1
    stats["total_requests"] += 1


@events.report_to_master.add_listener
def on_report_to_master(client_id, data):
    """
    This event is triggered on the worker instances every time a stats report is
    to be sent to the locust master. It will allow us to add our extra content-length
    data to the dict that is being sent, and then we clear the local stats in the worker.
    """
    data["total_requests"] = stats["total_requests"]
    for range_val in counters_keys:
        data[range_val] = counters[range_val]
        counters[range_val] = 0
    stats["total_requests"] = 0
    # counters["total_requests"] = 0


@events.worker_report.add_listener
def on_worker_report(client_id, data):
    """
    This event is triggered on the master instance when a new stats report arrives
    from a worker. Here we just add the content-length to the master's aggregated
    stats dict.
    """
    stats["total_requests"] += data["total_requests"]
    for range_val in counters_keys:
        counters[range_val] += data[range_val]
    print(stats)
    print(data)


@events.test_start.add_listener
def reset_counters(**kwargs):
    global counters, stats
    counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
    stats = {"total_requests": 0}

# Run the Locust test
# class MyUser(CustomUser):
#     wait_time = constant(int(ElevationConfig.wait_time))
