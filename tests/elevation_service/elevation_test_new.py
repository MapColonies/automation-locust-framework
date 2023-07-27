import json
from pathlib import Path

from locust import HttpUser, events, task

from common.config.config import ElevationConfig
from common.validation.validation_utils import (
    extract_file_type,
    write_rps_percent_results,
)

FILE_TYPE_JSON = "json"
FILE_TYPE_BIN = "bin"

POSITIONS_PATH = Path(ElevationConfig.positions_path)
RESULTS_PATH = ElevationConfig.results_path


class ResponseTimeCounter:
    def __init__(self):
        self.counter_range_1 = 0
        self.counter_range_2 = 0
        self.counter_range_3 = 0
        self.total_requests = 0

        # Define the response time ranges
        self.range_1 = (0, 100)
        self.range_2 = (101, 500)
        self.range_3 = (501, None)

    @events.request.add_listener
    def response_time_listener(self, response_time, **kwargs):
        if self.range_1[0] <= response_time <= self.range_1[1]:
            self.counter_range_1 += 1
        elif self.range_2[0] <= response_time <= self.range_2[1]:
            self.counter_range_2 += 1
        elif response_time >= self.range_3[0]:
            self.counter_range_3 += 1

        self.total_requests += 1

    @events.test_start.add_listener
    def reset_counters(self, **kwargs):
        self.counter_range_1 = 0
        self.counter_range_2 = 0
        self.counter_range_3 = 0
        self.total_requests = 0


def read_file(file_path):
    file_type = extract_file_type(file_path=file_path)
    if file_type == FILE_TYPE_JSON:
        with file_path.open() as file:
            body = json.load(file)
    elif file_type == FILE_TYPE_BIN:
        with file_path.open("rb") as file:
            body = file.read()
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    return file_type, body


class CustomUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_body = None
        self.counter = ResponseTimeCounter()

    def on_start(self):
        file_type, body = read_file(POSITIONS_PATH)
        self.request_body = {"request_type": file_type, "body": body}

    @task(1)
    def index(self):
        if self.request_body["request_type"] == FILE_TYPE_JSON:
            self.client.post(
                "/", json=self.request_body["body"], headers=ElevationConfig.headers
            )
        elif self.request_body["request_type"] == FILE_TYPE_BIN:
            self.client.post(
                "/", data=self.request_body["body"], headers=ElevationConfig.headers
            )

    def on_stop(self):
        # Calculate and present the percentage results
        percent_range_1 = (
            self.counter.counter_range_1 / self.counter.total_requests
        ) * 100
        percent_range_2 = (
            self.counter.counter_range_2 / self.counter.total_requests
        ) * 100
        percent_range_3 = (
            self.counter.counter_range_3 / self.counter.total_requests
        ) * 100

        percent_value_by_range = {
            f"{self.counter.range_1}": f"{percent_range_1}%",
            f"{self.counter.range_2}": f"{percent_range_2}%",
            f"{self.counter.range_3}": f"{percent_range_3}%",
            "total_requests": f"{self.counter.total_requests}",
        }
        write_rps_percent_results(
            custome_path=RESULTS_PATH, percente_value_by_range=percent_value_by_range
        )


class MyUser(CustomUser):
    min_wait = 100
    max_wait = 1000
