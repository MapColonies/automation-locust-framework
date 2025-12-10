from locust import HttpUser, task
from requests.adapters import HTTPAdapter
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
    def get_coverage_by_crs(self):
        subsets = self.wcs_client.get_subset(self.extent, self.axis_labels, self.is_degree)
        output_crs = self.wcs_client.generate_output_crs(config_obj["wcs"].OUTPUT_CRS, config_obj["wcs"].CRS_DICT)
        additional_params={
            "OUTPUTCRS": output_crs
        }

        res = self.wcs_client.get_coverage(self.coverage_id, config_obj["wcs"].FORMAT, subsets, self.session, additional_params)
