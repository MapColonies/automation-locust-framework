from datetime import datetime

from locust import HttpUser, task, events, between
import csv
import statistics

class CustomStatsWriter:
    def __init__(self, filename):
        self.filename = filename
        self.header = ["Range 1 (%)", "Range 2 (%)", "Range 3 (%)"]

    def write_csv_header(self, file):
        writer = csv.writer(file)
        writer.writerow(self.header)

    def write_stats(self, file, entries):
        writer = csv.writer(file)

        # Calculate response time ranges
        response_times = [entry[3] for entry in entries]
        min_response_time = min(response_times)
        max_response_time = max(response_times)
        range_1 = (min_response_time, min_response_time + (max_response_time - min_response_time) / 3)
        range_2 = (range_1[1], min_response_time + (max_response_time - min_response_time) * 2 / 3)
        range_3 = (range_2[1], max_response_time)

        # Calculate percentage values for response time ranges
        total_requests = len(entries)
        print(total_requests)
        range_1_requests = sum(1 for entry in entries if range_1[0] <= entry[3] < range_1[1])
        print(f"range_1_requests-------------{range_1_requests}")
        range_1_percent = (range_1_requests / total_requests) * 100
        range_2_requests = sum(1 for entry in entries if range_2[0] <= entry[3] < range_2[1])
        range_2_percent = (range_2_requests / total_requests) * 100
        range_3_requests = sum(1 for entry in entries if range_3[0] <= entry[3] <= range_3[1])
        range_3_percent = (range_3_requests / total_requests) * 100

        # Write the header row with custom column names
        writer.writerow(self.header + ["Range 1 (%)", "Range 2 (%)", "Range 3 (%)"])

        # Write the statistics data with response time percentages
        for entry in entries:
            row = list(entry)
            row += [range_1_percent, range_2_percent, range_3_percent]
            writer.writerow(row)

class MyUser(HttpUser):
    stats_writer = None
    wait_time = between(1, 3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats_writer = CustomStatsWriter("my_stats.csv")

    @task
    def my_task(self):
        self.client.get(url="https://www.ynet.co.il/home")

        # Perform tasks


    def on_start(self):
        # Open the stats file and write the header
        with open(self.stats_writer.filename, "w", newline="") as file:
            self.stats_writer.write_csv_header(file)

    def on_request_success(self, request_type, name, response_time, response_length):
        # Collect stats
        with open(self.stats_writer.filename, "a", newline="") as file:
            self.stats_writer.write_stats(file, [(self.get_current_timestamp(), request_type, name, response_time, response_length)])

    def get_current_timestamp(self):
        # Helper method to get the current timestamp
        # Replace with your preferred timestamp format
        return datetime.now().isoformat()

    def on_stop(self):
        # Additional logic when the test is stopped
        pass
