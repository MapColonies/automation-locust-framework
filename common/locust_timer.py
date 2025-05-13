from locust import constant, constant_throughput, between, constant_pacing

from common.config.config import config_obj
from common.utils.constants.strings import CONSTANT_TIMER_STR, BETWEEN_TIMER_STR, CONSTANT_PACING_TIMER_STR, \
    INVALID_TIMER_STR, CONSTANT_THROUGHPUT_TIMER_STR


def set_wait_time(timer_selection, wait_time):
    if timer_selection == 1:
        return constant(wait_time), CONSTANT_TIMER_STR
    elif timer_selection == 2:
        pass
        return constant_throughput(wait_time), CONSTANT_THROUGHPUT_TIMER_STR
    elif timer_selection == 3:
        return (
            between(config_obj["default"].MIN_WAIT, config_obj["default"].MAX_WAIT),
            BETWEEN_TIMER_STR,
        )
    elif timer_selection == 4:
        return constant_pacing(wait_time), CONSTANT_PACING_TIMER_STR
    else:
        return None, INVALID_TIMER_STR



