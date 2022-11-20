from locust import between
from locust import constant
from locust import constant_pacing
from locust import constant_throughput
from locust import HttpUser
from locust import task
from config.config import config_obj
from test_data.queries import POLYGON_XML, ID_RECORD_XML, REGION_RECORD_XML
from common.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)


class SizingUser(HttpUser):
    timer_selection = config_obj["default"].WAIT_TIME_FUNC
    wait_time = config_obj["default"].WAIT_TIME
    if timer_selection == 1:
        wait_time = constant(wait_time)
        print(CONSTANT_TIMER_STR)
    elif timer_selection == 2:
        wait_time = constant_throughput(wait_time)
        print(CONSTANT_THROUGHPUT_TIMER_STR)
    elif timer_selection == 3:
        wait_time = between(
            config_obj["default"].MIN_WAIT, config_obj["default"].MAX_WAIT
        )
        print(BETWEEN_TIMER_STR)
    elif timer_selection == 4:
        wait_time = constant_pacing(wait_time)
        print(CONSTANT_PACING_TIMER_STR)
    else:
        print(INVALID_TIMER_STR)

    @task(1)
    def get_records_by_polygon(self):
        polygon_request = self.client.post(
            "/",
            data=POLYGON_XML.encode("UTF-8"),
            verify=False,
        )

    @task(1)
    def get_records_by_id(self):
        id_record_request = self.client.post(
            "/",
            data=ID_RECORD_XML.encode("utf-8"),
            verify=False,
        )

    @task(1)
    def get_records_by_region(self):
        region_record_request = self.client.post(
            "/",
            data=REGION_RECORD_XML.encode("utf-8"),
            verify=False,
        )
