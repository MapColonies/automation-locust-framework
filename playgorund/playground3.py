def find_unmatched_tuples(input_dict, tuples_list):
    unmatched_tuples = []
    try:
        positions_data = input_dict.get("positions")
    except Exception as e:
        return e
    for item in positions_data:
        keys_values = (str(item["longitude"]), str(item["latitude"]))
        # keys_values = [item["longitude"], item["latitude"]]
        found_match = False
        for tuples_val in tuples_list:
            if keys_values[0] == str(tuples_val[0]) and keys_values[1] == str(tuples_val[1]):
                print(f"Matched values for {keys_values}")
                found_match = True  # Mark the match
                # Don't break, continue checking other tuples

        if not found_match:
            unmatched_tuples.append(keys_values)

    return unmatched_tuples


# Example usage:
dict1 = {'positions': [{'longitude': 34.992439347930606, 'latitude': 32.77572823596632},
                       {'longitude': 35.032773908445435, 'latitude': 32.77723204586287},
                       {'longitude': 34.975315094895336, 'latitude': 32.794120651131365},
                       {'longitude': 34.98164515034782, 'latitude': 32.78454041895311},
                       {'longitude': 35.0646058291626, 'latitude': 32.79635839294717}], 'productType': 'MIXED',
         'excludeFields': []}
x = [
    (34.992439347930606, 32.77572823596632),
    (35.032773908445435, 32.77723204586287),
    (34.975315094895336, 32.794120651131365),
    (34.98164515034782, 32.78454041895311),
    (35.0646058291626, 32.79635839294717)
]
# x = [
#     [34.992439347930606, 32.77572823596632],
#     [35.032773908445435, 32.77723204586287],
#     [34.975315094895336, 32.794120651131365],
#     [34.98164515034782, 32.78454041895311],
#     [35.0646058291626, 32.79635839294717]
# ]

print(find_unmatched_tuples(input_dict=dict1, tuples_list=x))


dict1 = {'check': [{'key1': 34.992439347930606, 'key2': 32.77572823596632},
                       {'key1': 35.032773908445435, 'key2': 32.77723204586287},
                       {'key1': 34.975315094895336, 'key2': 32.794120651131365},
                       {'key1': 34.98164515034782, 'key2': 32.78454041895311},
                       {'key1': 35.0646058291626, 'key2': 32.79635839294717}], 'check1': 'val',
         'check2': []}


