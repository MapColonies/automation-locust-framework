from locust import task, FastHttpUser, tag, between
from config.config import config_obj

#check bbox from EastBank
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
