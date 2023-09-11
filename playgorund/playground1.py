# def find_unmatched_tuples(input_dict, tuples_list):
#     unmatched_tuples = []
#     if "check" in input_dict and isinstance(input_dict["check"], list):
#         if len(input_dict["check"]) == len(tuples_list):
#             print("same lengths")
#
#         for item in input_dict["check"]:
#             print(item)
#             if "key1" in item and "key2" in item:
#                 key1_value = item["key1"]
#                 key2_value = item["key2"]
#                 keys_values = (key1_value, key2_value)
#                 for tuples_val in tuples_list:
#                     if keys_values == tuples_val:
#                         print(f"matched values for {keys_values}")
#                     else:
#                         unmatched_tuples.append(keys_values)

                # if keys_values not in tuples_list:
                #     unmatched_tuples.append((key1_value, key2_value))
    #
    # return unmatched_tuples
    #



# Example usage:
dict1 = {  # # Example usage:
    "check": [  # dict1 = {
        {"key1": 1, "key2": 2},  # "check": [
        {"key1": 3, "key2": 4},  # {"key1": 34.99329017908319, "key2": 32.75730973158232},
        {"key1": 5, "key2": 6},  # {"key1": 34.99798221083507, "key2": 32.79931519606793},
        {"key1": 7, "key2": 8},  # {"key1": 35.00240318612141, "key2": 32.7935654102479},
        {"key1": 9, "key2": 10}  # {"key1": 35.01469671603069, "key2": 32.78338486794766},
    ],  # {"key1": 35.04743080042179, "key2": 32.795414543794415}
    "field1": "check",  # ],
    "field2": []  # "field1": "check",
}  # "field2": []
# }
tuples_list = [  #
     (5, 6),# tuples_list = [
    (3, 4),  # (34.99329017908319, 32.75730973158232),
    (9, 10), # (34.99798221083507, 32.79931519606793),
    (7, 8),
    (1, 2)# (35.00240318612141, 32.7935654102479),
      # (35.01469671603069, 32.78338486794766),
]  # (35.04743080042179, 32.7954145437944151)
# ]
#


