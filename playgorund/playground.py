# x = {'results_47621.json': {'(0, 100)': 0, '(100, 500)': 3, '(500, inf)': 15},
#      'results_48619.json': {'(0, 100)': 24, '(100, 500)': 1, '(500, inf)': 0}}
# values = x.values()
# values = list(values)
# # print(values)
# # print(values[0])

import os
def sum_nested_dicts(nested_dict):
    result = {}

    for key, data_dict in nested_dict.items():
        for nested_key, value in data_dict.items():
            if nested_key in result:
                result[nested_key] += value
            else:
                result[nested_key] = value

    return result


# print(sum_nested_dicts(x))
