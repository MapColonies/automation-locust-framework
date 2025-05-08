from locust import FastHttpUser, task, constant
from common.config.config import config_obj
from common.utils.wfs_wrapper import WFSClient, GeoGenerator

geo_generator = GeoGenerator(ROI_PATH=config_obj["wfs"].ROI_PATH)


class GetFeatureByBboxUser(FastHttpUser):
    wait_time = constant(config_obj["wfs"].WAIT_TIME)

    @task
    def get_feature_by_intersects(self):
        my_client = WFSClient(base_url=config_obj["wfs"].WFS_URL, version=
        config_obj["wfs"].VERSION,
                              token=config_obj["wfs"].TOKEN)

        intersect_filter = my_client.create_intersects_filter(
            type_name="automation_2025_05_07_15_22_58-RasterVectorBest", pos_list=[34.48760376150682
                , 31.530834035809296
                , 34.48819410915064
                , 31.530834035809296
                , 34.48819410915064
                , 31.531043009844296
                , 34.48760376150682
                , 31.531043009844296
                , 34.48760376150682
                , 31.530834035809296])
        print(intersect_filter)
        my_client.session = self.client
        my_client.get_feature(filters=intersect_filter)
