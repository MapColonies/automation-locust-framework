import json
import random
from locust import FastHttpUser, task, constant
from common.config.config import config_obj
from common.utils.wfs_wrapper import WFSClient, GeoGenerator

geo_generator = GeoGenerator(ROI_PATH=config_obj["wfs"].ROI_PATH)
with open(config_obj["wfs"].ATTRIBUTE_MAPPING, "r") as f:
    attributes_mappings = json.load(f)


class GetFeatureByAttributeUser(FastHttpUser):
    wait_time = constant(config_obj["wfs"].WAIT_TIME)

    @task
    def get_feature_by_attribute(self):
        attribute = random.choice(attributes_mappings)
        my_client = WFSClient(base_url=config_obj["wfs"].WFS_URL, version=
        config_obj["wfs"].VERSION,
                              token=config_obj["wfs"].TOKEN)

        my_client.session = self.client
        attribute_filter = my_client.create_attribute_filter(attribute=attribute.get("attributeName"),
                                                             value=attribute.get("attributeValue"),
                                                             type_names=attribute.get("typeNames"))
        my_client.get_feature(filters=attribute_filter)
        my_client.session = self.client

