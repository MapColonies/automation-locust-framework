from locust import HttpUser, between, task
from prometheus_client import Counter, start_http_server

# Create a Prometheus counter to track successful requests
successful_requests = Counter(
    "locust_successful_requests", "Number of successful requests"
)


class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def my_task(self):
        # Send a request to your application
        response = self.client.get("https://www.ynet.co.il/home/")

        # Check the response and update the counter
        if response.status_code == 200:
            successful_requests.inc()


# Start the Prometheus metrics server
start_http_server(8080)

# # Run Locust
# MyUser().run()
