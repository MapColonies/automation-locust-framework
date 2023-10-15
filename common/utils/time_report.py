import datetime
import json
import threading

from common.config import custom_path

ranges = [100, 200, 300, 400, 500, float("inf")]


class TimeReport:
    def __init__(self, file_name):
        self.name = file_name
        # self.low = 0
        # self.med = 0
        # self.high = 0
        # ranges_values = []
        self.config_ranges = []
        self.counters = {}
        self.lock = threading.Lock()

    # def med_increase(self):
    #     with self.lock:
    #         self.med += 1
    #
    # def high_increase(self):
    #     with self.lock:
    #         self.high += 1
    #
    # def low_increase(self):
    #     with self.lock:
    #         self.low += 1
    def initiate_ranges_counters(self):
        sorted_ranges = sorted(self.config_ranges)

        # Using list comprehension to create a tuple of lower and upper numbers
        lower_upper_tuples = [
            (sorted_ranges[i], sorted_ranges[i + 1])
            for i in range(len(sorted_ranges) - 1)
        ]
        for i in lower_upper_tuples:
            self.counters[f"{i}"] = 0
        return self.counters

    def present(self):
        """ "
        The Function return the counter
        """
        return f"LOW: {self.low}, MID: {self.med}, High: {self.high}"

    def write_rps_percent_results(self):
        """
        this function writes the percent result of the request per second ranges to JSON that located in the given path
        :param percente_value_by_range: b
        :param custom_path: a path that provided by user
        :return:
        """
        json_obj = json.dumps(self.time_calculate())
        file_name = self.generate_unique_filename()
        with open(f"{custom_path}/{file_name}", "w") as f:
            f.write(json_obj)
        f.close()

    def generate_unique_filename(self):
        """
        this function generate unique name for runs results
        :return:
        """
        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")
        formatted_time = now.strftime("%H-%M-%S")
        filename = f"{self.name}_{formatted_date}_{formatted_time}.json"
        return filename

    def times_count(self, time):
        """
        The function receives a response time and increases the counter according to the desired ranges
        :return:
        """ ""
        for range_counter in self.config_ranges:
            if time < range_counter:
                self.config_ranges[str(rank)] += 1

    def time_calculate(self, total_requests):
        """
        This function sums up the counters and calculates the percentages after the end of the test
        :return:
        """ ""
        if total_requests != 0:
            for index, (key, value) in enumerate(self.config_ranges.items()):
                percent_range = (value / total_requests) * 100
                percent_value_by_range[f"{key}"] = percent_range

            return {
                "Low": self.low / total,
                "Med": self.med / total,
                "High": self.high / total,
                "Total": total,
            }
        else:
            return {"message": "Can't divide by Zero "}

    def reset_count(self):
        """
        This function resets the counters for the next run
        :return:
        """ ""
        self.lock = threading.Lock()
        return self


"""
--- Read me --
To use this utils in locust follow the next steps :
1. Add this file to your Projects
2 . add in your config file the custom_path= path in your system to local storage , low_time- minimum time until zero  , med_time - the meddile time
3. Add to your locust the next code :

obj_time = TimeReport(__name__)


@events.request.add_listener
def my_request_handler(request_type, name, response_time, response_length, response,
                       context, exception, start_time, url, **kwargs):
    obj_time.times_count(response_time)


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    obj_time.reset_count()
    if not isinstance(environment.runner, MasterRunner):
        print("Beginning test setup ")
    else:
        print("Started test from Master node")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if not isinstance(environment.runner, MasterRunner):
        print("Cleaning up test data" + obj_time.present())
        obj_time.write_rps_percent_results()
    else:
        print("Stopped test from Master node")


"""
