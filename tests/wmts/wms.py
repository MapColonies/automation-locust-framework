import logging

from locust import task, FastHttpUser, tag

from config.config import config_obj

bbox = [35.06068, 31.93225, 35.06270, 31.93316]
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


class User(FastHttpUser):


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


    # host = config_obj['wms'].HOST
    host = 'https://mapproxy-raster-qa-route-raster-qa.apps.j1lk3njp.eastus.aroapp.io/'
