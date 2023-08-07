from locust import HttpUser, between, constant, constant_pacing, task
from common.utils.csvreader import CSVReader

from common.config.config import Config, ProActiveConfig, WmtsConfig, config_obj
from common.utils.constants.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)
from tests.pycsw.test_data.queries import ID_RECORD_XML, POLYGON_XML, REGION_RECORD_XML


def set_wait_time(timer_selection, wait_time):
    if timer_selection == 1:
        return constant(wait_time), CONSTANT_TIMER_STR
    elif timer_selection == 2:
        pass
        # return constant_throughput(wait_time), CONSTANT_THROUGHPUT_TIMER_STR
    elif timer_selection == 3:
        return (
            between(config_obj["default"].MIN_WAIT, config_obj["default"].MAX_WAIT),
            BETWEEN_TIMER_STR,
        )
    elif timer_selection == 4:
        return constant_pacing(wait_time), CONSTANT_PACING_TIMER_STR
    else:
        return None, INVALID_TIMER_STR


wmts_csv_path = WmtsConfig.WMTS_CSV_PATH
ssn_reader = CSVReader(wmts_csv_path)


class PycswInquiries(HttpUser):
    pycsw_host = ProActiveConfig.pyscw_host

    @task(1)
    def get_records_by_polygon(self):
        self.client.post(
            "/",
            data=POLYGON_XML.encode("UTF-8"),
            params={"token": Config.TOKEN},
            verify=False,
        )

    @task(1)
    def get_records_by_id(self):
        self.client.post(
            "/",
            data=ID_RECORD_XML.encode("utf-8"),
            params={"token": Config.TOKEN},
            verify=False,
        )

    @task(1)
    def get_records_by_region(self):
        self.client.post(
            "/",
            data=REGION_RECORD_XML.encode("utf-8"),
            params={"token": Config.TOKEN},
            verify=False,
        )


class WmtsInquiries(HttpUser):
    wmts_host = ProActiveConfig.wmts_host

    @task
    def wmts_requests(self):
        # Task 2 logic goes here
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


class MyLocust(HttpUser):
    tasks = {WmtsInquiries: 1, PycswInquiries: 1}

    # Common tasks for all user behaviors can be defined here

    # def on_start(self):
    #     # Logic to execute when a user starts a task
    #     self.random_layers_tiles_urls = create_random_layers_urls()
    #     random.shuffle(self.random_layers_tiles_urls)
