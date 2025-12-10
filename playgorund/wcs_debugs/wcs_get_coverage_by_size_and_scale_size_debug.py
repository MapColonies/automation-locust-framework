import requests
from requests.adapters import HTTPAdapter
from common.config.config import config_obj
from common.utils.wcs_client import WCSClient

class NoNormHTTPAdapter(HTTPAdapter):
    def request_url(self, request, proxies):
        return request.url # Return exactly what the user gave – no normalization

if __name__ == "__main__":
    wcs_client = WCSClient(
        base_url=config_obj["wcs"].BASE_URL,
        version=config_obj["wcs"].VERSION,
        token=config_obj["wcs"].TOKEN
    )
    session = requests.Session()
    session.mount("https://", NoNormHTTPAdapter())

    coverage_id = config_obj["wcs"].COVERAGE_ID
    layer_xml = wcs_client.get_describe_coverage(coverage_id, session)
    extent, axis_labels, is_degree = wcs_client.parse_coverage_metadata(layer_xml)


    subsets = wcs_client.get_subset(extent, axis_labels, is_degree)
    scale_size = wcs_client.generate_scalesize(config_obj["wcs"].SCALE_SIZE)
    additional_params={
        "SCALESIZE": scale_size
    }
    res = wcs_client.get_coverage(coverage_id, config_obj["wcs"].FORMAT, subsets, session, additional_params)