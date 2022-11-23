from common.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)
from config.config import config_obj
from locust import (
    HttpUser,
    between,
    constant,
    constant_pacing,
    constant_throughput,
    task,
)
from test_data.queries import ID_RECORD_XML, POLYGON_XML, REGION_RECORD_XML


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
        self.client.post(
            "/",
            data=POLYGON_XML.encode("UTF-8"),
            verify=False,
        )

    @task(1)
    def get_records_by_id(self):
        self.client.post(
            "/",
            data=ID_RECORD_XML.encode("utf-8"),
            verify=False,
        )

    @task(1)
    def get_records_by_region(self):
        self.client.post(
            "/",
            data=REGION_RECORD_XML.encode("utf-8"),
            verify=False,
        )
