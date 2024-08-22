from locust import HttpUser, constant, events, task
from common.config.config import config_obj
from common.utils.csvreader import CSVReader
from common.utils.data_generator.data_utils import custom_sorting_key
from common.validation.validation_utils import (
    find_range_for_response_time,
    initiate_counters_by_ranges,
    retype_env
)

if isinstance(config_obj["_3d"].percent_ranges, str):
    percent_ranges = retype_env(config_obj["_3d"].percent_ranges)
    percent_ranges.append(0)
    percent_ranges.append(float("inf"))
    percent_ranges = sorted(percent_ranges)
else:
    percent_ranges = config_obj["_3d"].percent_ranges
    percent_ranges.append(0)
    percent_ranges.append(float("inf"))
    percent_ranges = sorted(percent_ranges)

counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
counters_keys = list(counters.keys())

ssn_reader = CSVReader(config_obj["_3d"].CSV_DATA_PATH)
# ssn_reader = CSVReader(
#     "/home/shayavr/Desktop/git/automation-locust-framework/test_data/filtered_urls.csv")
# results_path = config_obj["_3d"].RESULTS_PATH

if isinstance(config_obj["wmts"].WAIT_TIME, str):
    wait_time = retype_env(config_obj["wmts"].WAIT_TIME)
else:
    wait_time = config_obj["wmts"].WAIT_TIME


class User(HttpUser):
    wait_time = constant(wait_time)

    @task(1)
    def index(self):
        url = next(ssn_reader)
        self.client.get(url=url[0], verify=False)

        # if content_type != "application/octet-stream":
        #     response.failure(f"Invalid response content-type: {content_type}")
        # elif response.status_code == 402 or response.status_code == 403 or response.status_code == 401:
        #     response.failure(f"status code: {response.status_code} for: {url[1]}")

        host = config_obj["default"].HOST


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

            if requests_amount != 0:
                for index, (key, value) in enumerate(counters.items()):
                    percent_range = (value / requests_amount) * 100
                    percent_value_by_range[f"{key}"] = percent_range

                # percent_value_by_range["total_requests"] = int(requests_amount)
                # print(percent_value_by_range)
                percent_value_by_range = dict(sorted(percent_value_by_range.items(), key=custom_sorting_key))
            return {"percent_value": percent_value_by_range,
                    "total_requests": stats["total_requests"]}


# create counters for each range value from the configuration


@events.test_start.add_listener
def on_locust_init(environment, **_kwargs):
    environment.users_count = environment.runner.target_user_count


@events.request.add_listener
def response_time_listener(response_time, **kwargs):
    global counters
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


@events.test_start.add_listener
def reset_counters(**kwargs):
    global counters, total_requests, stats
    counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
    total_requests = 0
    stats = {"total_requests": 0}
