from locust import HttpUser, task, events
from locust.stats import StatsCSVFileWriter, RequestStats


class MyUser(HttpUser):
    wait_time = 1

    @task
    def my_task(self):
        self.client.get("/")
        # Send requests
        # ...



    def stats_csv_writer(self, file_path):
        writer = StatsCSVFileWriter.stats_writer(file_path)

        # Add custom column name to the CSV header
        writer.writerow(writer.header + ["ResponseTimePercentage"])

        # Return the modified writer
        return writer


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    # Initialize custom statistics tracking
    environment.stats.response_times_within_range = {100: 0, 500: 0, 1000: 0}  # Example range: 100ms, 500ms, 1000ms

@events.request_success.add_listener
def on_request_success(request_type, name, response_time, response_length, **kwargs):
    # Increment response time count for the corresponding range
    for range_time in RequestStats.response_times_within_range:
        if response_time <= range_time:
            RequestStats.response_times_within_range[range_time] += 1
            break

@events.quitting.add_listener
def on_locust_quitting(environment, **kwargs):
    # Calculate and update the percentage in the CSV report
    total_requests = environment.stats.num_requests
    for range_time in RequestStats.response_times_within_range:
        count = RequestStats.response_times_within_range[range_time]
        percentage = (count / total_requests) * 100 if total_requests > 0 else 0
        environment.stats.get(name=None, method=None).append(percentage)