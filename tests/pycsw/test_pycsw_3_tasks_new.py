from locust import (
    HttpUser,
    between,
    constant,
    constant_pacing,
    constant_throughput,
    task,
)
from test_data.queries import ID_RECORD_XML, POLYGON_XML, REGION_RECORD_XML

from common.config.config import config_obj
from common.utils.constants.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)


class SizingUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        default_config = config_obj["DEFAULT"]
        self.wait_time = default_config.WAIT_TIME

        timer_funcs = {
            1: (constant(self.wait_time), CONSTANT_TIMER_STR),
            2: (constant_throughput(self.wait_time), CONSTANT_THROUGHPUT_TIMER_STR),
            3: (
                between(default_config.MIN_WAIT, default_config.MAX_WAIT),
                BETWEEN_TIMER_STR,
            ),
            4: (constant_pacing(self.wait_time), CONSTANT_PACING_TIMER_STR),
        }

        self.wait_time, timer_str = timer_funcs.get(
            default_config.WAIT_TIME_FUNC, (self.wait_time, INVALID_TIMER_STR)
        )
        print(timer_str)

    def post_task(self, data):
        self.client.post("/", data=data.encode("UTF-8"), verify=False)

    @task(1)
    def get_records_by_polygon(self):
        self.post_task(POLYGON_XML)

    @task(1)
    def get_records_by_id(self):
        self.post_task(ID_RECORD_XML)

    @task(1)
    def get_records_by_region(self):
        self.post_task(REGION_RECORD_XML)
