import json
import random

from locust import FastHttpUser, task, constant
from common.config.config import config_obj
from common.utils.wfs_wrapper import WFSClient, GeoGenerator


with open(config_obj["wfs"].BBOX_MAPPING, "r") as f:
    bbox_mappings = json.load(f)

class GetFeatureByIntersectsUser(FastHttpUser):
    wait_time = constant(config_obj["wfs"].WAIT_TIME)

    @task
    def get_feature_by_intersects(self):
        mapping = random.choice(bbox_mappings)
        geo_generator = GeoGenerator(ROI_PATH=mapping.get("roiPath"))
        polygon = geo_generator.generate_random_polygon(vertex_count=5)
        print(polygon)
        my_client = WFSClient(base_url=config_obj["wfs"].WFS_URL, version=
        config_obj["wfs"].VERSION,
                              token=config_obj["wfs"].TOKEN)

        intersect_filter = my_client.create_intersects_filter(
            type_name=mapping.get("typeName"), pos_list=polygon)
        print(intersect_filter)
        my_client.session = self.client
        my_client.get_feature(filters=intersect_filter)
