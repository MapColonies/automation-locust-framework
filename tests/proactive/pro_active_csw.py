from locust import (
    HttpUser,
    between,
    constant,
    constant_pacing,
    task,
)

from common.config.config import config_obj
from common.utils.constants.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)
from tests.pycsw.test_data.queries import ID_RECORD_XML, POLYGON_XML, REGION_RECORD_XML


def set_wait_time(timer_selection, wait_time):
    if timer_selection == 1:
        return constant(wait_time), CONSTANT_TIMER_STR
    elif timer_selection == 2:
        return constant_throughput(wait_time), CONSTANT_THROUGHPUT_TIMER_STR
    elif timer_selection == 3:
        return (
            between(config_obj["default"].MIN_WAIT, config_obj["default"].MAX_WAIT),
            BETWEEN_TIMER_STR,
        )
    elif timer_selection == 4:
        return constant_pacing(wait_time), CONSTANT_PACING_TIMER_STR
    else:
        return None, INVALID_TIMER_STR


class SizingUser(HttpUser):
    """
    A Locust user class that simulates requests made by sizing users.
    """

    timer_selection = config_obj["default"].WAIT_TIME_FUNC
    wait_time = config_obj["default"].WAIT_TIME

    wait_time, timer_message = set_wait_time(timer_selection, wait_time)
    print(timer_message)

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
