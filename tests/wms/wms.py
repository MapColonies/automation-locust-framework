from locust import task, FastHttpUser, tag, between, events
from config.config import config_obj
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

# check bbox from EastBank
bbox = config_obj['wms'].BBOX
delta_x = bbox[3] - bbox[1]
delta_y = bbox[2] - bbox[0]

wmstileT = lambda \
        l: f"api/raster/v1/service?LAYERS={config_obj['wms'].LAYER_TYPE}&FORMAT={config_obj['wms'].WMS_FORMAT}&SRS={config_obj['wms'].SRS}" \
           f"&service=wms&version={config_obj['wms'].WMS_VERSION}&REQUEST=GetMap&STYLES={config_obj['wms'].STYLE}" \
           f"&BBOX={str.format('{:6f}', l[0])},{str.format('{:6f}', l[1])},{str.format('{:6f}', l[2])},{str.format('{:6f}', l[3])}&WIDTH={config_obj['wms'].WIDTH}" \
           f"&HEIGHT={config_obj['wms'].HEIGHT}&token={config_obj['wms'].TOK}"

wmstileNoToken = lambda \
        l: f"api/raster/v1/service?LAYERS={config_obj['wms'].LAYER_TYPE}&FORMAT={config_obj['wms'].WMS_FORMAT}&SRS={config_obj['wms'].SRS}" \
           f"&service=wms&version={config_obj['wms'].WMS_VERSION}&REQUEST=GetMap&STYLES={config_obj['wms'].STYLE}" \
           f"&BBOX={str.format('{:6f}', l[0])},{str.format('{:6f}', l[1])},{str.format('{:6f}', l[2])},{str.format('{:6f}', l[3])}&WIDTH={config_obj['wms'].WIDTH}" \
           f"&HEIGHT={config_obj['wms'].HEIGHT}"


class User(FastHttpUser):
    host = config_obj['wms'].HOST
    between(1, 1)

    @task(1)
    @tag('regular')
    def zoom_level_up(self):
        bbox[0] += 0.00006
        bbox[1] += 0.00006
        bbox[2] += 0.00006
        bbox[3] += 0.00006
        if config_obj['wms'].IS_TOKEN:
            self.client.get(wmstileT(bbox))
        else:
            self.client.get(wmstileNoToken(bbox))

    @task(1)
    @tag('zoom')
    def zoom_delta(self):
        if config_obj['wms'].IS_UPSCALE:
            zoom = bbox
            zoom[2] -= delta_y
            zoom[3] -= delta_x
            if config_obj['wms'].IS_TOKEN:
                self.client.get(wmstileT(zoom))
            else:
                self.client.get(wmstileNoToken(zoom))

    # host = 'https://mapproxy-raster-qa-route-raster-qa.apps.j1lk3njp.eastus.aroapp.io/' __name__ #'


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
