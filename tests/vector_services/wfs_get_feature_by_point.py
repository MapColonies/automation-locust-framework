import logging
import random
from locust import FastHttpUser, task, constant
from common.config.config import config_obj
from common.utils.wfs_wrapper import WFSClient, GeoGenerator

geo_generator = GeoGenerator(ROI_PATH=config_obj["wfs"].ROI_PATH)
logger = logging.getLogger("locust.user")


class GetFeatureByPointUser(FastHttpUser):
    wait_time = constant(config_obj["wfs"].WAIT_TIME)

    @task
    def get_feature_by_point(self):
        radius = random.randint(config_obj["wfs"].MIN_RADIUS, config_obj["wfs"].MAX_RADIUS)
        point = ' , '.join(map(str, geo_generator.get_random_point()))

        my_client = WFSClient(base_url=config_obj["wfs"].WFS_URL, version=
        config_obj["wfs"].VERSION,
                              token=config_obj["wfs"].TOKEN)

        point_filter = my_client.create_wfs_point_dwithin_filter_body(point=point, distance=radius)
        logger.info(f"Point filter: {point_filter}")
        my_client.session = self.client
        my_client.get_feature(filters=point_filter)
        my_client.session = self.client
