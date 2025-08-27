from locust import FastHttpUser, task, constant
from common.config.config import config_obj
from common.utils.wfs_wrapper import WFSClient, GeoGenerator


class WFSUser(FastHttpUser):
    wait_time = constant(config_obj["wfs"].WAIT_TIME)

    def on_start(self):
        # Init your WFSClient here with your configuration
        self.wfs_client = WFSClient(base_url=config_obj["wfs"].WFS_URL, version=
        config_obj["wfs"].VERSION,
                                    token=config_obj["wfs"].TOKEN)

        self.geo_generator = GeoGenerator(ROI_PATH=config_obj["wfs"].ROI_PATH)
        self.type_name = config_obj["wfs"].TYPE_NAME  # update with actual type name

    @task
    def get_feature_count(self):
        # Create intersects filter around random polygon for spatial filtering
        polygon = self.geo_generator.generate_random_polygon(vertex_count=config_obj["wfs"].VERTEX_COUNT)
        if polygon:
            xml_body = self.wfs_client.create_intersects_filter(polygon, self.type_name)
            try:
                response = self.wfs_client.get_feature(
                    filters=xml_body,
                    request_params={"resultType": "hits"}
                )
                print(response.text)
                print(f"Feature count: {response.json().get("numberMatched")}")
            except Exception as e:
                print(f"Failed to retrieve feature count: {e}")
