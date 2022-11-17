from common.strings import (
    BETWEEN_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    CONSTANT_TIMER_STR,
    INVALID_TIMER_STR,
)
from config import Selection, config , WmtsConfig
from locust import (
    HttpUser,
    between,
    constant,
    constant_pacing,
    constant_throughput,
    task,
)
from locust_plugins.csvreader import CSVReader

wmts_csv_path = WmtsConfig.WMTS_CSV_PATH
ssn_reader = CSVReader(wmts_csv_path)


class User(HttpUser):
    timer_selection = config[Selection.WMTS].WAIT_TIME_FUNC
    wait_time = config[Selection.WMTS].WAIT_TIME
    if timer_selection == 1:
        wait_time = constant(wait_time)
        print(CONSTANT_TIMER_STR)
    elif timer_selection == 2:
        wait_time = constant_throughput(wait_time)
        print(CONSTANT_THROUGHPUT_TIMER_STR)
    elif timer_selection == 3:
        wait_time = between(
            config[Selection.WMTS].MIN_WAIT, config[Selection.WMTS].MAX_WAIT
        )
        print(BETWEEN_TIMER_STR)
    elif timer_selection == 4:
        wait_time = constant_pacing(wait_time)
        print(CONSTANT_PACING_TIMER_STR)
    else:
        print(INVALID_TIMER_STR)

    @task(1)
    def index(self):
        points = next(ssn_reader)
        if config[Selection.WMTS].TOKEN is None:
            self.client.get(
                f"/{config[Selection.WMTS].LAYER_TYPE}/"
                f"{config[Selection.WMTS].LAYER_NAME}/"
                f"{config[Selection.WMTS].GRID_NAME}/"
                f"{points[0]}/{points[1]}/{points[2]}"
                f"{config[Selection.WMTS].IMAGE_FORMAT}",
            )
        else:
            self.client.get(
                f"/{config[Selection.WMTS].LAYER_TYPE}/"
                f"{config[Selection.WMTS].LAYER_NAME}/"
                f"{config[Selection.WMTS].GRID_NAME}/"
                f"{points[0]}/{points[1]}/{points[2]}"
                f"{config[Selection.WMTS].IMAGE_FORMAT}"
                f"?token={config[Selection.WMTS].TOKEN}",
            )

    host = config[Selection.WMTS].HOST
