from locust import User, task, events, HttpUser


class CustomUser(HttpUser):
    host = "https://www.ynet.co.il/home"

    @task
    def my_task(self):
        response = self.client.get("/")
        # Process the response as needed

    def on_stop(self):
        # Calculate and present the percentage results
        percent_range_1 = (counter_range_1 / total_requests) * 100
        percent_range_2 = (counter_range_2 / total_requests) * 100
        percent_range_3 = (counter_range_3 / total_requests) * 100

        print(f"Percentage of requests in range {range_1}: {percent_range_1}%")
        print(f"Percentage of requests in range {range_2}: {percent_range_2}%")
        print(f"Percentage of requests in range {range_3}: {percent_range_3}%")
        print(total_requests)

# Define the response time counters
counter_range_1 = 0
counter_range_2 = 0
counter_range_3 = 0
total_requests = 0

# Define the response time ranges
range_1 = (0, 100)
range_2 = (101, 500)
range_3 = (501, None)

# Define the response time event hook
@events.request.add_listener
def response_time_listener(request_type, name, response_time, **kwargs):
    global counter_range_1, counter_range_2, counter_range_3, total_requests

    if range_1[0] <= response_time <= range_1[1]:
        counter_range_1 += 1
    elif range_2[0] <= response_time <= range_2[1]:
        counter_range_2 += 1
    elif response_time >= range_3[0]:
        counter_range_3 += 1

    total_requests += 1
@events.test_start.add_listener
def reset_counters(**kwargs):
    global counter_range_1, counter_range_2, counter_range_3, total_requests

    counter_range_1 = 0
    counter_range_2 = 0
    counter_range_3 = 0
    total_requests = 0

# Run the Locust test
class MyUser(CustomUser):
    min_wait = 100
    max_wait = 1000




