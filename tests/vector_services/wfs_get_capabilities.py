from locust import FastHttpUser, task, constant
from common.config.config import config_obj
from common.utils.wfs_wrapper import WFSClient


class GetCapabilitiestUser(FastHttpUser):
    wait_time = constant(config_obj["wfs"].WAIT_TIME)

    @task
    def get_capabilities(self):
        my_client = WFSClient(base_url=config_obj["wfs"].HOST, version=
        config_obj["wfs"].VERSION,
                              token=config_obj["wfs"].TOKEN)
        my_client.session = self.client
        my_client.get_capabilities()
