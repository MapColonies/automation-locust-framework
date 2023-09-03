import bisect
from typing import List


def initiate_counters_by_ranges(config_ranges: List) -> dict:
    """
    this function will extract the ranges and counter values for each value of range on the configuration
    :param config_ranges: selected configuration ranges
    :return:
    counter for each range (dict): counter for each given range
    """
    sorted_ranges = sorted(config_ranges)

    # Using list comprehension to create a tuple of lower and upper numbers
    lower_upper_tuples = [
        (sorted_ranges[i], sorted_ranges[i + 1]) for i in range(len(sorted_ranges) - 1)
    ]
    print("lower_upper_tuples", lower_upper_tuples)
    counters = {}
    for i in lower_upper_tuples:
        counters[f"{i}"] = 0
    return counters


def find_range_for_number(number, sorted_list, counters_dict):
    index = bisect.bisect_left(sorted_list, number)
    print(index)

    # If the index is 0, the number is smaller than the first element in the list
    if index == 0:
        range_value = str((None, sorted_list[0]))
        counters_dict[range_value] += 1

    # If the index is equal to the list length, the number is greater than the last element in the list
    if index == len(sorted_list):
        range_value = str((sorted_list[-1], None))
        counters_dict[range_value] += 1

    # Otherwise, the number is located between two elements in the list
    lower_bound = sorted_list[index - 1]
    upper_bound = sorted_list[index]

    range_value = str((lower_bound, upper_bound))
    counters_dict[range_value] += 1

    return counters_dict


percent_ranges = [100, 500]
percent_ranges.append(0)
percent_ranges.append(float("inf"))

# Example usage
sorted_list = sorted(percent_ranges)
print(initiate_counters_by_ranges(sorted_list))
counter1 = initiate_counters_by_ranges(sorted_list)
# print(sorted_list)

number_1 = 600
x = find_range_for_number(number_1, sorted_list, counter1)
print(x)


# print("new function working", initiate_counters_by_ranges(percent_ranges))

# def check_resp_time_by_range(rsp_time, )
