# my_locust_test.py
from locust import HttpUser, task, events
from logger import log_request, shutdown_logger

class MyUser(HttpUser):
    @task
    def my_task(self):
        payload = {"key": "value"}
        params = {"q": "search"}
        self.client.post("/endpoint", json=payload, params=params)

        log_request("POST", "/endpoint", params, payload)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    shutdown_logger()
