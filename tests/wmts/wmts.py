from config.config import WmtsConfig, config_obj
from locust import FastHttpUser, between, tag, task
from locust_plugins.csvreader import CSVReader

wmts_csv_path = WmtsConfig.WMTS_CSV_PATH

ssn_reader = CSVReader(wmts_csv_path)


class User(FastHttpUser):
    between(1, 1)

    @task(
        1
    )  # #WMTS - “HTTP_REQUEST_TYPE /SUB_DOMAIN/PROTOCOL/LAYER/TILE_MATRIX_SET/Z/X/Y.IMAGE_FORMAT HTTP_VERSION“
    @tag("wmts-loading")
    def index(self):
        points = next(ssn_reader)
        if config_obj["wmts"].IS_TOKEN:
            self.client.get(
                f"/{config_obj['wmts'].LAYER_TYPE}/"
                f"{config_obj['wmts'].LAYER_NAME}/"
                f"{config_obj['wmts'].GRID_NAME}/"
                f"{points[0]}/{points[1]}/{points[2]}"
                f"{config_obj['wmts'].IMAGE_FORMAT}",
                f"?token={config_obj['wmts'].TOKEN}",
            )
        else:
            self.client.get(
                f"/{config_obj['wmts'].LAYER_TYPE}/"
                f"{config_obj['wmts'].LAYER_NAME}/"
                f"{config_obj['wmts'].GRID_NAME}/"
                f"{points[0]}/{points[1]}/{points[2]}"
                f"{config_obj['wmts'].IMAGE_FORMAT}"
            )

    host = "https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1"
