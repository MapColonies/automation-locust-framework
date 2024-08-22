import os
import sys
from pathlib import Path

from locust import (
    FastHttpUser,
    between,
    constant,
    constant_pacing,
    constant_throughput,
    events,
    task,
)

from common.config.config import WmtsConfig, config_obj
# from common.utils import (
#     count_rsp_time_by_rsp_time_ranges,
#     extract_response_time_from_record,
#     get_percentile_value,
#     write_rsp_time_percentile_ranges,
# )
from common.utils import (
    count_rsp_time_by_rsp_time_ranges,
    extract_response_time_from_record,
    get_percentile_value,
    write_rsp_time_percentile_ranges,
)
from common.utils.constants.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)
from common.utils.csvreader import CSVReader
from common.validation.validation_utils import initiate_counters_by_ranges, find_range_for_response_time

myDir = os.getcwd()
sys.path.append(myDir)

path = Path(myDir)
a = str(path.parent.absolute())
sys.path.append(a)

wmts_csv_path = WmtsConfig.WMTS_CSV_PATH
ssn_reader = CSVReader(wmts_csv_path)

if isinstance(config_obj["_3d"].percent_ranges, str):
    percent_ranges = eval(config_obj["_3d"].percent_ranges)
    percent_ranges.append(0)
    percent_ranges.append(float("inf"))
    percent_ranges = sorted(percent_ranges)
else:
    percent_ranges = config_obj["_3d"].percent_ranges
    percent_ranges.append(0)
    percent_ranges.append(float("inf"))
    percent_ranges = sorted(percent_ranges)

stat_file = open("stats.csv", "w")
wmts_csv_path = WmtsConfig.WMTS_CSV_PATH
ssn_reader = CSVReader(wmts_csv_path)

counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
print(counters)
counters_keys = list(counters.keys())

def set_wait_time(timer_selection, wait_time):
    if timer_selection == 1:
        return constant(wait_time), CONSTANT_TIMER_STR
    elif timer_selection == 2:
        return constant_throughput(wait_time), CONSTANT_THROUGHPUT_TIMER_STR
    elif timer_selection == 3:
        return (
            between(config_obj["wmts"].MIN_WAIT, config_obj["wmts"].MAX_WAIT),
            BETWEEN_TIMER_STR,
        )
    elif timer_selection == 4:
        return constant_pacing(wait_time), CONSTANT_PACING_TIMER_STR
    else:
        return None, INVALID_TIMER_STR


class User(FastHttpUser):
    timer_selection = config_obj["wmts"].WAIT_TIME_FUNC
    wait_time = config_obj["wmts"].WAIT_TIME
    timer_selection = config_obj["wmts"].WAIT_TIME_FUNC[0]
    wait_time = config_obj["wmts"].WAIT_TIME[0]

    wait_time, timer_message = set_wait_time(timer_selection, wait_time)
    print(timer_message)

    @task(1)
    def index(self):
        points = next(ssn_reader)
        url = (
            f"/{config_obj['wmts'].LAYER_TYPE}/"
            f"{config_obj['wmts'].LAYER_NAME}/"
            f"{config_obj['wmts'].GRID_NAME}/"
            f"{points[0]}/{points[1]}/{points[2]}"
            f"{config_obj['wmts'].IMAGE_FORMAT}"
        )
        if config_obj["wmts"].TOKEN:
            url += f"?token={config_obj['wmts'].TOKEN}"
        self.client.get(url)

    host = config_obj["wmts"].HOST


@events.test_start.add_listener
def on_locust_init(environment, **_kwargs):
    environment.users_count = environment.runner.target_user_count


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
    global counters, total_requests, stats
    counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
    total_requests = 0
    stats = {"total_requests": 0}

    def on_stop(self):
        rsp_list = extract_response_time_from_record(
            csv_path=config_obj["wmts"].REQUESTS_RECORDS_CSV
        )
        percentile_rages_dict = {}
        rsp_time_ranges = [(0, 100), (101, 500), (501, None)]
        for idx, rsp_t_range in enumerate(rsp_time_ranges):
            counter = count_rsp_time_by_rsp_time_ranges(
                rsp_time_data=rsp_list, rsp_range=rsp_t_range
            )

            percentile = get_percentile_value(
                rsp_counter=counter, rsp_time_list=rsp_list
            )
            percentile_rages_dict[str(rsp_time_ranges[idx])] = percentile
        write_rsp_time_percentile_ranges(percentile_rages_dict)


@events.request.add_listener
def hook_request_(request_type, name, response_time, response_length, response, **kw):
    stat_file.write(
        str(response)
        + ";"
        + request_type
        + ";"
        + name
        + ";"
        + str(response_time)
        + ";"
        + str(response_length)
        + "\n"
    )


@events.quitting.add_listener
def hook_quitting(environment, **kw):
    stat_file.close()
