# This file contains constants related to wait timers.

# Constant wait time strategy: This strategy uses a fixed wait time for each iteration.
CONSTANT_TIMER_STR = "Choosing constant wait time"

# Constant throughput wait time strategy: This strategy adjusts wait time based on desired throughput.
CONSTANT_THROUGHPUT_TIMER_STR = "Choosing constant throughput wait time"

# Between wait time strategy: This strategy selects wait time between a specified range for each iteration.
BETWEEN_TIMER_STR = "Choosing between wait time"

# Constant pacing wait time strategy: This strategy maintains a constant pace by adjusting wait time dynamically.
CONSTANT_PACING_TIMER_STR = "Choosing constant pacing wait time"

# Invalid wait function: This is returned when an invalid wait strategy is selected.
INVALID_TIMER_STR = "Invalid wait function"
