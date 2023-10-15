# import json
# from json import JSONDecodeError
#
# from locust import HttpUser, task
# class Tasks(HttpUser):
#     @task
#     def task(self):
#         with self.client.get("https://www.ynet.co.il") as response:
#             try:
#                 result = json.loads(response.content)
#                 if len(result["result"]) == 0:
#                     response.failure(result)
#                     # log.error(result)
#             except (TypeError, JSONDecodeError) as err:
#                 response.failure(response.text)
# log.error(f'{type(err).__name__} because of : {response.status_code} - {response.text}')


#
# from locust import HttpUser, task
#
# class MyUser(HttpUser):
#     @task
#     def my_task(self):
#         response = self.client.get("https://www.ynet.co.il")
#
#         # Check the response content type
#         content_type = response.headers.get("Content-Type", "")
#
#         if "application/json" not in content_type:
#             # Mark the request as a failure with a custom reason including the response text
#             response.failure(f"Content-Type is not text/html. Response: {response.text}")
#
# from locust import HttpUser, task
#
#
# class MyUser(HttpUser):
#     @task
#     def my_task(self):
#         response = self.client.get("https://www.ynet.co.il")
#
#         # Check the response content type
#         content_type = response.headers.get("Content-Type", "")
#
#         if "application/json" not in content_type:
#             # Mark the request as a failure with a custom reason including the response text
#             failure_reason = f"Content-Type is not text/html. Response: {response.text}"
#             response.failure(failure_reason)


# from locust import HttpUser, task
#
#
# class MyUser(HttpUser):
#     @task
#     def my_task(self):
#         with self.client.get("https://www.ynet.co.il", catch_response=True) as response:
#             content_type = response.headers.get("Content-Type", "")
#             if content_type != "application/json":
#                 response.failure("Not a json")
#             elif response.elapsed.total_seconds() > 0.5:
#                 response.failure("Request took too long")
# todo: option 1
#
# dict1 = {'geeks': 5, 'gfg': 1, 'is': 2, 'for': 4, 'best!': 3}
# dict2 = {'geeks': 5, 'gfg': 2, 'is': 3, 'for': 7, 'best': 3}
#
# # get common keys in both dictionaries
# common_keys = set(dict1.keys()) & set(dict2.keys())
# x = ['for', 'geeks', 'is', 'gfg']
# x = set(x)
# print(x)
# print(type(x))
#
# # create sets of values for common keys in both dictionaries
# dict1_values = {dict1[key] for key in common_keys}
# dict2_values = {dict2[key] for key in common_keys}
#
# # check if both sets of values are equal
# if dict1_values == dict2_values:
#     print("Dictionaries are equal")
# else:
#     print("Dictionaries are not equal")

list_1 = [{"longitude": 34.98822939269719, "latitude": 32.770895713204006},
          {"longitude": 35.05318626126633, "latitude": 32.76247057096294},
          {"longitude": 35.01068099807608, "latitude": 32.76125136785018}]
list_2 = [
    {
        "latitude": 32.770895713204006,
        "longitude": 34.9882293926972,
        # "height": 205.39599743019247,
        # "productType": "QUANTIZED_MESH_DTM_BEST",
        # "updateDate": "2023-05-08T17:44:01.000Z",
        # "resolutionMeter": 30
    },
    {
        "latitude": 32.76247057096294,
        "longitude": 35.05318626126633,
        # "height": 31.224700682487267,
        # "productType": "QUANTIZED_MESH_DTM_BEST",
        # "updateDate": "2023-05-08T17:44:01.000Z",
        # "resolutionMeter": 30
    },
    {
        "latitude": 32.76125136785018,
        "longitude": 35.01068099807608,
        # "height": 353.1207129640256,
        # "productType": "QUANTIZED_MESH_DTM_BEST",
        # "updateDate": "2023-05-08T17:44:01.000Z",
        # "resolutionMeter": 30
    }
]
pairs = zip(list_1, list_2)
print(pairs)
if any(x != y for x, y in pairs):
    print("diff")



def find_unmatched_points(response_output: dict, requests_points: dict):
    """
    :param response_output: service heights response dict
    :param requests_points: request body that contain the requested points lat long value
    :return:
    list of unmatched points if exist
    """
    unmatched_tuples = []
    try:
        response_output = dict(response_output)
        positions_data = response_output["data"]
    except Exception as e:
        return e
    requests_points = dict(requests_points)
    requests_points_list = requests_points["positions"]
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
    print("unmatched_points", unmatched_tuples)
    return unmatched_tuples
