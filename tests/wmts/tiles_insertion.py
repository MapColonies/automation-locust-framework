from locust import FastHttpUser, task, constant
from locust_plugins.csvreader import CSVReader

from common.config.config import config_obj, WmtsConfig

wmts_csv_path = WmtsConfig.WMTS_CSV_PATH
ssn_reader = CSVReader(wmts_csv_path)

class User(FastHttpUser):
    
    wait_time = constant(1)

    @task(1)
    def index(self):
        points = next(ssn_reader)
        url = (
            f"/{config_obj['wmts'].LAYER_TYPE}/"
            f"{config_obj['wmts'].LAYER_NAME}/"
            f"{config_obj['wmts'].GRID_NAME}/"
            f"{points[0]}/{points[1]}/{points[2]}"
            f"{config_obj['wmts'].IMAGE_FORMAT}"
        )
        if config_obj["wmts"].TOKEN:
            url += f"?token={config_obj['wmts'].TOKEN}"
        self.client.get(url)

    host = config_obj["wmts"].HOST