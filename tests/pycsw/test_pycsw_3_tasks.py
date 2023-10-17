from config.config import config_obj, Config
from locust import between, task, FastHttpUser, tag, events

from test_data.queries import QUERY_TEMPLATE
from config.config import Config
from common.percentiles_utils import (find_range_for_response_time,
                                      initiate_counters_by_ranges,
                                      retype_env, custom_sorting_key
                                      )

if type(Config.percent_ranges) == str:
    percent_ranges = list(Config.percent_ranges)
else:
    percent_ranges = Config.percent_ranges

stats = {"total_requests": 0}
counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
counters_keys = list(counters.keys())
polygon = {'name': config_obj["pycsw"].PYCSW_POLYGON_PROPERTY, 'value': config_obj["pycsw"].PYCSW_POLYGON_VALUE}
by_id = {'name': config_obj["pycsw"].PYCSW_ID_PROPERTY, 'value': config_obj["pycsw"].PYCSW_ID_VALUE}
by_region = {'name': config_obj["pycsw"].PYCSW_REGION_PROPERTY, 'value': config_obj["pycsw"].PYCSW_REGION_VALUE}


class SizingUser(FastHttpUser):
    between(1, 1)

    @tag("GetRecordsByPolygon")
    @task(1)
    def get_records_by_polygon(self):
        if config_obj["pycsw"].TOKEN_FLAG:
            self.client.post(
                f"?token={config_obj['pycsw'].Token}",
                data=QUERY_TEMPLATE(polygon).encode("UTF-8"),
                verify=False,
            )
        else:
            self.client.post(
                "/",
                data=QUERY_TEMPLATE(polygon).encode("utf-8"),
                verify=False,
            )

    @tag("GetRecordsByID")
    @task(1)
    def get_records_by_id(self):
        if config_obj["pycsw"].TOKEN_FLAG:
            self.client.post(
                f"?token={config_obj['pycsw'].Token}",
                data=QUERY_TEMPLATE(by_id).encode("utf-8"),
                verify=False,
            )
        else:
            self.client.post(
                "/",
                data=QUERY_TEMPLATE(by_id).encode("utf-8"),
                verify=False,
            )

    @tag("GetRecordsByRegion")
    @task(1)
    def get_records_by_region(self):
        if config_obj["pycsw"].TOKEN_FLAG:
            self.client.post(
                f"?token={config_obj['pycsw'].Token}",
                data=QUERY_TEMPLATE(by_region).encode("utf-8"),
                verify=False,
            )
            self.client.post(
                "/",
                data=QUERY_TEMPLATE(by_region).encode("utf-8"),
                verify=False,
            )
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
    counters = find_range_for_response_time(
        response_time=response_time, ranges_list=percent_ranges, counters_dict=counters
    )
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
    global counters, stats
    counters = initiate_counters_by_ranges(config_ranges=percent_ranges)
    stats = {"total_requests": 0}
