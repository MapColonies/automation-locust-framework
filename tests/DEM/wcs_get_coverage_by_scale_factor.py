from locust import HttpUser, task
from requests.adapters import HTTPAdapter
from shapely.affinity import scale

from common.config.config import config_obj
from common.utils.wcs_client import WCSClient

class NoNormHTTPAdapter(HTTPAdapter):
    def request_url(self, request, proxies):
        return request.url # Return exactly what the user gave – no normalization

class WCSGetCoverageUser(HttpUser):
    host = config_obj["wcs"].BASE_URL

    def on_start(self):
        self.wcs_client = WCSClient(
            base_url=config_obj["wcs"].BASE_URL,
            version=config_obj["wcs"].VERSION,
            token=config_obj["wcs"].TOKEN
        )
        self.session = self.client #get to request.session()
        self.session.mount("https://", NoNormHTTPAdapter())

        self.coverage_id = config_obj["wcs"].COVERAGE_ID
        self.layer_xml = self.wcs_client.get_describe_coverage(self.coverage_id, self.session)
        self.extent, self.axis_labels, self.is_degree = self.wcs_client.parse_coverage_metadata(self.layer_xml)

    @task
    def get_coverage_by_scale_size(self):
        subsets = self.wcs_client.get_subset(self.extent, self.axis_labels, self.is_degree)
        scale_factor = config_obj["wcs"].SCALE_FACTOR
        additional_params={
            "scalefactor": scale_factor
        }
        res = self.wcs_client.get_coverage(self.coverage_id, config_obj["wcs"].FORMAT, subsets, self.session, additional_params)