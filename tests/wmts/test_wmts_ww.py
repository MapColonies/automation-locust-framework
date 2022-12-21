from common.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)
from config.config import WmtsConfig, config_obj
from locust import (
    FastHttpUser,
    between,
    constant,
    constant_pacing,
    constant_throughput,
    task,
)
from locust_plugins.csvreader import CSVReader

wmts_csv_path = WmtsConfig.WMTS_CSV_PATH
ssn_reader = CSVReader(wmts_csv_path)


class User(FastHttpUser):
    wait_time = constant_pacing(1)

    @task(1)
    def index(self):
        points = next(ssn_reader)
        if config_obj["wmts"].TOKEN is None:
            self.client.get(
                f"/{config_obj['wmts'].LAYER_TYPE}/"
                f"{config_obj['wmts'].LAYER_NAME}/"
                f"{config_obj['wmts'].GRID_NAME}/"
                f"{points[0]}/{points[1]}/{points[2]}"
                f"{config_obj['wmts'].IMAGE_FORMAT}",
            )
        else:
            self.client.get(
                f"/{config_obj['wmts'].LAYER_TYPE}/"
                f"{config_obj['wmts'].LAYER_NAME}/"
                f"{config_obj['wmts'].GRID_NAME}/"
                f"{points[0]}/{points[1]}/{points[2]}"
                f"{config_obj['wmts'].IMAGE_FORMAT}"
                f"?token={config_obj['wmts'].TOKEN}",
            )

    host = config_obj["wmts"].HOST
