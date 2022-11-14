from locust_plugins.csvreader import CSVReader
from locust import HttpUser, constant, constant_throughput, between, constant_pacing
from config import Selection, config
from common.strings import (
    CONSTANT_TIMER_STR,
    CONSTANT_PACING_TIMER_STR,
    CONSTANT_THROUGHPUT_TIMER_STR,
    BETWEEN_TIMER_STR,
    INVALID_TIMER_STR,
)

ssn_reader = CSVReader("csv_data/data/new.csv")


class User(HttpUser):
    timer_selection = config[Selection.WMTS].WAIT_TIME_FUNC
    wait_time = config[Selection.WMTS].WAIT_TIME
    if timer_selection == 1:
        wait_time = constant(wait_time)
        print(CONSTANT_TIMER_STR)
    elif timer_selection == 2:
        wait_time = constant_throughput(wait_time)
        print(CONSTANT_THROUGHPUT_TIMER_STR)
    elif timer_selection == 3:
        wait_time = between(cfg.MIN_WAIT, cfg.MAX_WAIT)
        print(BETWEEN_TIMER_STR)
    elif timer_selection == 4:
        wait_time = constant_pacing(wait_time)
        print(CONSTANT_PACING_TIMER_STR)
    else:
        print(INVALID_TIMER_STR)
