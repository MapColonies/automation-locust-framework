import json
import random
from locust import FastHttpUser, task, constant
from common.config.config import config_obj
from common.utils.wfs_wrapper import WFSClient


if isinstance(config_obj["wfs"].ID_LIST,str):
    gf_ids = json.loads(config_obj["wfs"].ID_LIST)
elif isinstance(config_obj["wfs"].ID_LIST,list):
    gf_ids = config_obj["wfs"].ID_LIST
else:
    raise TypeError


class GetFeatureByIdUser(FastHttpUser):
    wait_time = constant(config_obj["wfs"].WAIT_TIME)


    @task
    def get_feature_by_id(self):
        feature_id = random.choice(gf_ids)
        my_client = WFSClient(base_url=config_obj["wfs"].WFS_URL, version=
        config_obj["wfs"].VERSION,
                              token=config_obj["wfs"].TOKEN)
        my_client.session = self.client
        my_client.get_feature(request_params={"featureID": feature_id})
