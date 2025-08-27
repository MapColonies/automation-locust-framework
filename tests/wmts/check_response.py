from locust import FastHttpUser, task, constant
from locust_plugins.csvreader import CSVReader

from common.config.config import config_obj, WmtsConfig

wmts_csv_path = WmtsConfig.WMTS_CSV_PATH
ssn_reader = CSVReader(wmts_csv_path)

expected_bytes = bytes.fromhex("636865636B")  # "check"

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
        with self.client.get(url,catch_response=True) as response:
            body_text = response.text or ""        # safe default
            body_bytes = response.content or b""   # safe default

            if "check" in body_text or b"check" in body_bytes:
                response.success()
            else:
                response.failure("Response did not contain 'check'")

    host = config_obj["wmts"].HOST