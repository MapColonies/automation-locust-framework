import random
from locust import FastHttpUser, task, constant
from common.config.config import config_obj
from common.utils.wfs_wrapper import WFSClient, GeoGenerator

geo_generator = GeoGenerator(ROI_PATH=config_obj["wfs"].ROI_PATH)


class GetFeatureByAttributeUser(FastHttpUser):
    wait_time = constant(config_obj["wfs"].WAIT_TIME)

    @task
    def get_feature_by_attribute(self):
        my_client = WFSClient(base_url=config_obj["wfs"].WFS_URL, version=
        config_obj["wfs"].VERSION,
                              token=config_obj["wfs"].TOKEN)

        my_client.session = self.client
        #todo: change the function according to the json structure
        attribute_filter = my_client.create_attribute_filter(attribute="",value="",type_names="")
        print(attribute_filter)
        my_client.get_feature(filters=attribute_filter)

        my_client.session = self.client
