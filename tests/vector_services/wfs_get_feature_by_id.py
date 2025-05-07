import random
from locust import FastHttpUser, task, constant
from common.config.config import config_obj
from common.utils.wfs_wrapper import WFSClient


class GetFeatureByIdUser(FastHttpUser):
    wait_time = constant(config_obj["wfs"].WAIT_TIME)

    def on_start(self):
        # Assign each user a random ID from the list
        self.feature_id = random.choice(config_obj["wfs"].ID_LIST)

    @task
    def get_feature_by_id(self):
        my_client = WFSClient(base_url=config_obj["wfs"].WFS_URL, version=
        config_obj["wfs"].VERSION,
                              token=config_obj["wfs"].TOKEN)
        my_client.session = self.client
        my_client.get_feature(request_params={"featureID": self.feature_id})
