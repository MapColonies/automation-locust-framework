from locust import between, constant, constant_pacing, constant_throughput


class TimerStrings:
    BETWEEN_TIMER_STR = "BETWEEN_TIMER"
    CONSTANT_PACING_TIMER_STR = "CONSTANT_PACING_TIMER"
    CONSTANT_THROUGHPUT_TIMER_STR = "CONSTANT_THROUGHPUT_TIMER"
    CONSTANT_TIMER_STR = "CONSTANT_TIMER"
    INVALID_TIMER_STR = "INVALID_TIMER"

    @staticmethod
    def set_wait_time(timer_selection, wait_time):
        if timer_selection == 1:
            return constant(wait_time), TimerStrings.CONSTANT_TIMER_STR
        elif timer_selection == 2:
            return (
                constant_throughput(wait_time),
                TimerStrings.CONSTANT_THROUGHPUT_TIMER_STR,
            )
        elif timer_selection == 3:
            return (
                between(wait_time["min_wait"], wait_time["max_wait"]),
                TimerStrings.BETWEEN_TIMER_STR,
            )
        elif timer_selection == 4:
            return constant_pacing(wait_time), TimerStrings.CONSTANT_PACING_TIMER_STR
        else:
            return None, TimerStrings.INVALID_TIMER_STR
