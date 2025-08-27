import json
import logging
import random
from locust import FastHttpUser, task, constant
from common.config.config import config_obj
from common.utils.wfs_wrapper import WFSClient, GeoGenerator

with open(config_obj["wfs"].BBOX_MAPPING, "r") as f:
    bbox_mappings = json.load(f)

logger = logging.getLogger("locust.user")


class GetFeatureByBboxUser(FastHttpUser):
    wait_time = constant(config_obj["wfs"].WAIT_TIME)

    @task
    def get_feature_by_bbox(self):
        mapping = random.choice(bbox_mappings)
        logger.info(f"mapping is {mapping}"),
        geo_generator = GeoGenerator(ROI_PATH=mapping.get("roiPath"))
        bbox = geo_generator.get_random_bbox(min_width=config_obj["wfs"].MIN_WIDTH,
                                             max_width=config_obj["wfs"].MAX_WIDTH,
                                             min_height=config_obj["wfs"].MIN_HEIGHT,
                                             max_height=config_obj["wfs"].MAX_HEIGHT)
        bbox = f"{bbox}, EPSG:4326"
        logger.info(f"bbox value: {bbox}")
        my_client = WFSClient(base_url=config_obj["wfs"].WFS_URL, version=
        config_obj["wfs"].VERSION,
                              token=config_obj["wfs"].TOKEN)
        my_client.session = self.client
        my_client.get_feature(method="POST", request_params={"bbox": bbox,
                                                            "typeNames": mapping.get("typeName")})
        # my_client.get_feature(method=config_obj["wfs"].REQUEST_METHOD, request_params={"bbox": bbox,
        #                                                     "typeNames": mapping.get("typeName")})
