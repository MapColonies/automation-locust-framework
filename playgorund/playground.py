# x = {'results_47621.json': {'(0, 100)': 0, '(100, 500)': 3, '(500, inf)': 15},
#      'results_48619.json': {'(0, 100)': 24, '(100, 500)': 1, '(500, inf)': 0}}
# values = x.values()
# values = list(values)
# # print(values)
# # print(values[0])

# import os
# import sys
# from pathlib import Path
#
# myDir = os.getcwd()
# sys.path.append(myDir)
#
# path = Path(myDir)
# a = str(path.parent.absolute())
# sys.path.append(a)
def sum_nested_dicts(nested_dict):
    result = {}

    for key, data_dict in nested_dict.items():
        for nested_key, value in data_dict.items():
            if nested_key in result:
                result[nested_key] += value
            else:
                result[nested_key] = value

    return result

#
# x = {'results_47621.json': {'(0, 100)': 0, '(100, 500)': 3, '(500, inf)': 15, "total_requests": 15},
#      'results_48619.json': {'(0, 100)': 24, '(100, 500)': 1, '(500, inf)': 0, "total_requests": 10}}
#
# # print(sum_nested_dicts(x))
#
# stats = {"total_requests": 25}
# counters = {'(0, 100)': 24, '(100, 500)': 1, '(500, inf)': 0}
# requests_amount = stats["total_requests"]
# percent_value_by_range = {}
# if requests_amount != 0:
#     for key, value in counters.items():
#         print(key, value)
#         percent_range = (value / requests_amount) * 100
#         percent_value_by_range[f"{key}"] = percent_range
#
#     percent_value_by_range["total_requests"] = int(requests_amount)
#     print(percent_value_by_range)
