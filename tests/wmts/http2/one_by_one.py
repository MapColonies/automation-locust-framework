from config.config import config_obj
from locust import between, task, tag
from locust_plugins.csvreader import CSVReader
from utils.ClinetX import HttpxUser
ssn_reader = CSVReader(config_obj["wmts"].ONE_BY_ONE_RECORDS)


class User(HttpxUser):
    between(1, 1)
    host = config_obj["wmts"].HOST

    @tag("OneByOneRequest")
    @task(1)
    def index(self):
        url = next(ssn_reader)
        self.client.get(url=url[0], verify=False)
