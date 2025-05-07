import random
from locust import FastHttpUser, task, constant
from common.config.config import config_obj
from common.utils.wfs_wrapper import WFSClient, GeoGenerator

geo_generator = GeoGenerator(ROI_PATH=config_obj["wfs"].ROI_PATH)


class GetFeatureByIdUser(FastHttpUser):
    wait_time = constant(config_obj["wfs"].WAIT_TIME)

    def on_start(self):
        # Assign each user a random ID from the list
        self.bbox = geo_generator.get_random_bbox()

    @task
    def get_feature_by_id(self):
        my_client = WFSClient(base_url=config_obj["wfs"].WFS_URL, version=
        config_obj["wfs"].VERSION,
                              token=config_obj["wfs"].TOKEN)
        my_client.session = self.client
        my_client.get_feature(request_params={"bbox": self.bbox,
                                              "typeNames": config_obj["wfs"].TYPE_NAMES})
