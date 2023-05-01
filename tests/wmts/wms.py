from locust import task, FastHttpUser

from config.config import config_obj

bbox=[-19.86328125, -36.38671875, 91.58203125, 69.08203125]


class User (FastHttpUser):
    #if config_obj['WmsConfig'].TOKEN  is not None:

    @task(1)  # #WMTS - “HTTP_REQUEST_TYPE /SUB_DOMAIN/PROTOCOL/LAYER/TILE_MATRIX_SET/Z/X/Y.IMAGE_FORMAT HTTP_VERSION“
    def index(self):
        wmstile = lambda l: f"/api/raster/v1/service?LAYERS={config_obj['WmsConfig'].LAYER_TYPE}&FORMAT=image%2Fpng&SRS=EPSG%3A4326" \
               f"&EXCEPTIONS=application%2Fvnd.ogc.se_inimage" \
               f"&TRANSPARENT=TRUE&service=wms&VERSION=1.1.1&REQUEST=GetMap&STYLES=" \
               f"&BBOX={l[0]},{l[1]},{l[2]},{l[3]}&WIDTH={config_obj['WmsConfig'].WIDTH}" \
               f"&HEIGHT={config_obj['WmsConfig'].HEIGHT}&" \
               f"token={config_obj['wmsConfig'].TOK}"
        bbox[0] += 0.000005
        bbox[1] += 0.000005
        bbox[2] += 0.000005
        bbox[3] += 0.000005
        resp = self.client.get(wmstile(bbox))
        print(resp.info())

    host = 'https://mapproxy-raster-qa-route-raster-qa.apps.j1lk3njp.eastus.aroapp.io'












'api/raster/v1/service?LAYERS=dev-test-transparent-Orthophoto&FORMAT=image%2Fpng&SRS=EPSG%3A4326&EXCEPTIONS=application%252Fvnd.ogc.se_inimage&TRANSPARENT=TRUE&service=wms&VERSION=1.1.1&REQUEST=GetMap&STYLES=&BBOX=-19.86328125%2C-36.38671875%2C91.58203125%2C69.08203125&WIDTH=1920&HEIGHT=1080&token=eyJhbGciOiJSUzI1NiIsImtpZCI6Ik1hcENvbG9uaWVzUUEifQ.eyJkIjpbInJhc3RlciIsInJhc3RlcldtcyIsInJhc3RlckV4cG9ydCIsImRlbSIsInZlY3RvciIsIjNkIl0sImlhdCI6MTY2Mzg2MzM0Mywic3ViIjoiTWFwQ29sb25pZXNRQSIsImlzcyI6Im1hcGNvbG9uaWVzLXRva2VuLWNsaSJ9.U_sx0Rsy96MA3xpIcWQHJ76xvK0PlHa--J1YILBYm2fCwtDdM4HLGagwq-OQQnBqi2e8KwktQ7sgt27hOJIPBHuONQS0ezBbuByk6UqN2S7P8WERdt8_lejuR1c94owQq7FOkhEaj_PKJ64ehXuMMHskfNeAIBf8GBN6QUGEenVx2w5k2rYBULoU30rpFkQVo8TtmiK2yGx0Ssx2k6LqSgCZfyZJbFzZ2MH3BPeCVleP1-zypaF9DS7SxS-EutL-gZ1e9bEccNktxQA4VMcjeTv45KYJLTIrccs_8gtPlzfaeNQFTIUKD-cRD1gyd_uLatPsl0wwHyFZIgRuJtcvfw'
