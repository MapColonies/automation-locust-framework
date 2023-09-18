def find_unmatched_points(response_output: dict, requests_points: dict):
    """

    :param response_output: service heights response dict
    :param requests_points: request body that contain the requested points lat long value
    :return:
    list of unmatched points if exist 
    """
    unmatched_tuples = []

    try:
        positions_data = response_output.get("data")
    except Exception as e:
        return e
    requests_points_list = requests_points.get("positions")
    for item in positions_data:
        response_longitude = item["longitude"]
        response_latitude = item["latitude"]

        found_match = False
        for requests_points_data in requests_points_list:
            if requests_points_data["longitude"] == response_longitude and \
                    requests_points_data["latitude"] == response_latitude:
                print(f"Matched values for {[response_longitude, response_latitude]}")
                found_match = True  # Mark the match
                # Don't break, continue checking other tuples

        if not found_match:
            unmatched_tuples.append([response_longitude, response_latitude])

    return unmatched_tuples


# Example usage:
# dict1 = {'positions': [{'longitude': 34.992439347930606, 'latitude': 32.77572823596632},
#                        {'longitude': 35.032773908445435, 'latitude': 32.77723204586287},
#                        {'longitude': 34.975315094895336, 'latitude': 32.794120651131365},
#                        {'longitude': 34.98164515034782, 'latitude': 32.78454041895311},
#                        {'longitude': 35.0646058291626, 'latitude': 32.79635839294717}], 'productType': 'MIXED',
#          'excludeFields': []}

data = {
    "data": [
        {
            "latitude": 30.593996683761883,
            "longitude": 34.79320163300719,
            "height": None
        },
        {
            "latitude": 30.61286246725918,
            "longitude": 34.85981574220827,
            "height": None
        },
        {
            "latitude": 30.604152,
            "longitude": 34.864913,
            "height": None
        },
        {
            "latitude": 30.61126059265362,
            "longitude": 34.83523619872231,
            "height": None
        }
    ]
}
# x = [
#     (34.992439347930606, 32.775728235966321),
#     (35.032773908445435, 32.77723204586287),
#     (34.975315094895336, 32.794120651131365),
#     (34.98164515034782, 32.78454041895311),
#     (35.0646058291626, 32.79635839294717)
# ]


x = {"positions": [{"latitude": 30.5939966983761883,
                    "longitude": 34.79320163300719},
                   {"latitude": 30.61286246725918,
                    "longitude": 34.85981574220827, },
                   {"latitude": 30.604152149556473,
                    "longitude": 34.86491260959997},
                   {"latitude": 30.61126059265362,
                    "longitude": 34.83523619872231}], "productType": "MIXED",
     "excludeFields": []}
# x = [
#     [34.992439347930606, 32.77572823596632],
#     [35.032773908445435, 32.77723204586287],
#     [34.975315094895336, 32.794120651131365],
#     [34.98164515034782, 32.78454041895311],
#     [35.0646058291626, 32.79635839294717]
# ]

print(find_unmatched_points(response_output=data, requests_points=x))

# dict1 = {'check': [{'key1': 34.992439347930606, 'key2': 32.77572823596632},
#                    {'key1': 35.032773908445435, 'key2': 32.77723204586287},
#                    {'key1': 34.975315094895336, 'key2': 32.794120651131365},
#                    {'key1': 34.98164515034782, 'key2': 32.78454041895311},
#                    {'key1': 35.0646058291626, 'key2': 32.79635839294717}], 'check1': 'val',
#          'check2': []}

from decimal import Decimal

# x = str(32.77572823596632)
# my_float = 32.77572823596632
#
# import numpy as np
#
# # float32
# # float comparison
# num1 = np.float64(32.77572823596632)
# num2 = np.float64(32.775728235966321)
#
# print(num1 == num2)


from decimal import *

getcontext().prec = 28

# x = Decimal(1) / Decimal(7)
# print(x)
# Decimal('0.1428571428571428571428571429')
# def compareFloatNum(a, b):
#     # Correct method to compare
#     # floating-point numbers
#     if (abs(a - b) < 1e-9):
#         print("The numbers are equal ")
#     else:
#         print("The numbers are not equal ")
#
#
# # Driver code
# if __name__ == '__main__':
#     num1 = np.float64(32.77572823596632)
#     num2 = np.float64(32.775728235966321)
#     compareFloatNum(num1, num2)
#
#
# import pandas as pd
# import numpy as np
#
# df = pd.DataFrame({'A': [1.23456789, 1.234567891, 1.234567892]})
# tol = 1e-9
#
# mask = np.isclose(df['A'], 1.234567891, rtol=tol, atol=tol)
# df_filtered = df[mask]
# print(df_filtered)
