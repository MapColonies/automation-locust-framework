from locust import HttpUser, task, between
import httpx
from httpx import Client as http2client
import select
print(select.epoll)


class MyTaskSet(HttpUser):
    between(2, 2)

    def client(self):
        return http2client(http2=True)

    @task
    def my_task(self):
        response = self.client.get("/")
        print(response)

    def on_stop(self):
        self.client.close()


class MyUser(HttpUser):
    host = "https://www.google.com"
