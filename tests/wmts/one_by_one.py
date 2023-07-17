from config.config import config_obj
from locust import FastHttpUser, between, tag, task
from locust_plugins.csvreader import CSVReader

ssn_reader = CSVReader(config_obj["wmts"].ONE_BY_ONE_RECORDS)


class User(FastHttpUser):
    between(1, 1)
    host = config_obj["wmts"].HOST

    @tag("OneByOneRequest")
    @task(1)
    def index(self):
        url = next(ssn_reader)
        self.client.get(url=url[0], verify=False)
