import os
import httpx
from hyper.contrib import HTTP20Adapter
from locust import task, FastHttpUser, tag, HttpUser, events
from hyper import HTTP20Connection
from utils.ClientX import HttpxUser
from config.config import config_obj
from utils.percentile_calculation import write_rsp_time_percentile_ranges, count_rsp_time_by_rsp_time_ranges, \
    extract_response_time_from_record, get_percentile_value
import time


file_name = __name__ + '-stats.csv'
stat_file = open(file_name, 'w')
bbox = config_obj['wms'].BBOX
delta_x = bbox[3] - bbox[1]
delta_y = bbox[2] - bbox[0]

wmstileT = lambda l: f"api/raster/v1/service?LAYERS={config_obj['wms'].LAYER_TYPE}&FORMAT=image%2Fpng&SRS=EPSG%3A4326" \
                     f"&EXCEPTIONS=application%252Fvnd.ogc.se_inimage" \
                     f"&TRANSPARENT=TRUE&service=wms&VERSION=1.1.1&REQUEST=GetMap&STYLES=" \
                     f"&BBOX={l[0]}%2C{l[1]}%2C{l[2]}%2C{l[3]}&WIDTH={config_obj['wms'].WIDTH}" \
                     f"&HEIGHT={config_obj['wms'].HEIGHT}&token={config_obj['wms'].TOK}"

wmstileNoToken = lambda \
        l: f"api/raster/v1/service?LAYERS={config_obj['wms'].LAYER_TYPE}&FORMAT=image%2Fpng&SRS=EPSG%3A4326" \
           f"&EXCEPTIONS=application%252Fvnd.ogc.se_inimage" \
           f"&TRANSPARENT=TRUE&service=wms&VERSION=1.1.1&REQUEST=GetMap&STYLES=" \
           f"&BBOX={l[0]}%2C{l[1]}%2C{l[2]}%2C{l[3]}&WIDTH={config_obj['wms'].WIDTH}" \
           f"&HEIGHT={config_obj['wms'].HEIGHT}"

if config_obj['wms'].WEB_MERCATOR_FLAG:
    wmstileT += '&web-mercator=true'
    wmstileNoToken += '&web-mercator=true'


class User(HttpxUser):
    host = config_obj['wms'].HOST

    @task(1)
    @tag('regular')
    def zoom_level_up(self):
        bbox[0] += 0.00005
        bbox[1] += 0.00005
        bbox[2] += 0.00005
        bbox[3] += 0.00005
        if config_obj['wms'].TOKEN is True:
            resp = self.client.get(wmstileT(bbox))
        else:
            resp = self.client.get(wmstileNoToken(bbox))

    @task(1)
    @tag('zoom')
    def zoom_delta(self):
        zoom = bbox
        zoom[2] -= delta_y
        zoom[3] -= delta_x
        if config_obj['wms'].TOKEN is True:
            resp = self.client.get(wmstileT(zoom))
        else:
            resp = self.client.get(wmstileNoToken(zoom))

    # host = 'https://mapproxy-raster-qa-route-raster-qa.apps.j1lk3njp.eastus.aroapp.io/' __name__ #'
    def on_stop(self):
        rsp_list = extract_response_time_from_record(
            csv_path=file_name)

        # rsp_list_millisecond = convert_to_millisecond(response_time_list=rsp_list)
        percentile_rages_dict = {}
        rsp_time_ranges = [(0, 100), (101, 500), (501, None)]
        for idx, rsp_t_range in enumerate(rsp_time_ranges):
            counter = count_rsp_time_by_rsp_time_ranges(rsp_time_data=rsp_list, rsp_range=rsp_t_range)

            percentile = get_percentile_value(rsp_counter=counter, rsp_time_list=rsp_list)
            percentile_rages_dict[str(rsp_time_ranges[idx])] = percentile
        write_rsp_time_percentile_ranges(percentile_rages_dict, str(__name__))


@events.request.add_listener
def hook_request_success(request_type, name, response_time, response_length, response, **kw):
    stat_file.write(str(response) + ";" + request_type + ";" + name + ";" + str(response_time) + ";" + str(
        response_length) + "\n")


@events.quitting.add_listener
def hook_quitting(environment, **kw):
    stat_file.close()
