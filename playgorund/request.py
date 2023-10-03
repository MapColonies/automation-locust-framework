import json

from common.validation.validation_utils import validate_json_array_length

response = {
    "data": [
        {
            "latitude": 32.64652516994386,
            "longitude": 35.447053828916516,
            "height": 47.00070192571795,
            "productType": "QUANTIZED_MESH_DTM_BEST",
            "updateDate": "2023-05-08T17:44:01.000Z",
            "resolutionMeter": 30
        },
        {
            "latitude": 32.82904469399577,
            "longitude": 35.64699542549536,
            "height": None ,
            "productType": "QUANTIZED_MESH_DTM_BEST",
            "updateDate": "2023-05-08T17:44:01.000Z",
            "resolutionMeter": 30
        },
        {
            "latitude": 32.673555855449656,
            "longitude": 35.220768323815435,
            "height": 105.85939232711353,
            "productType": "QUANTIZED_MESH_DTM_BEST",
            "updateDate": "2023-05-08T17:44:01.000Z",
            "resolutionMeter": 30
        },
        {
            "latitude": 32.89247701323737,
            "longitude": 35.35842246078898,
            "height": 163.91012846547812,
            "productType": "QUANTIZED_MESH_DTM_BEST",
            "updateDate": "2023-05-08T17:44:01.000Z",
            "resolutionMeter": 30
        },
        {
            "latitude": 32.72041411066213,
            "longitude": 35.69904013547482,
            "height": -15.45560160635803,
            "productType": "QUANTIZED_MESH_DTM_BEST",
            "updateDate": "2023-05-08T17:44:01.000Z",
            "resolutionMeter": 30
        },
        {
            "latitude": 32.63017337551658,
            "longitude": 35.69309679511719,
            "height": 114.09297288607529,
            "productType": "QUANTIZED_MESH_DTM_BEST",
            "updateDate": "2023-05-08T17:44:01.000Z",
            "resolutionMeter": 30
        },
        {
            "latitude": 32.79841226884138,
            "longitude": 35.7531621092792,
            "height": 0,
            "productType": "QUANTIZED_MESH_DTM_BEST",
            "updateDate": "2023-04-21T23:44:41.000Z",
            "resolutionMeter": 100
        },
        {
            "latitude": 32.93811947392775,
            "longitude": 35.68476539869581,
            "height": 126.46374756487941,
            "productType": "QUANTIZED_MESH_DTM_BEST",
            "updateDate": "2023-05-08T17:44:01.000Z",
            "resolutionMeter": 30
        },
        {
            "latitude": 32.73263731993841,
            "longitude": 35.507807610366946,
            "height": -77.79577402185888,
            "productType": "QUANTIZED_MESH_DTM_BEST",
            "updateDate": "2023-05-08T17:44:01.000Z",
            "resolutionMeter": 30
        },
        {
            "latitude": 32.64618073579551,
            "longitude": 35.43338514787784,
            "height": 95.5707352343938,
            "productType": "QUANTIZED_MESH_DTM_BEST",
            "updateDate": "2023-05-08T17:44:01.000Z",
            "resolutionMeter": 30
        }
    ]
}
requests_positions = {
    "positions": [{"longitude": 35.447053828916516, "latitude": 32.64652516994386},
                  {"longitude": 35.64699542549536, "latitude": 32.82904469399577},
                  {"longitude": 35.220768323815435, "latitude": 32.673555855449656},
                  {"longitude": 35.7531621092792, "latitude": 32.79841226884138},
                  {"longitude": 35.35842246078898, "latitude": 32.89247701323737},
                  {"longitude": 35.69904013547482, "latitude": 32.72041411066213},
                  {"longitude": 35.69309679511719, "latitude": 32.63017337551658},
                  {"longitude": 35.68476539869581, "latitude": 32.93811947392775},
                  {"longitude": 35.507807610366946, "latitude": 32.73263731993841},
                  {"longitude": 35.43338514787784, "latitude": 32.64618073579551}], "productType": "MIXED",
    "excludeFields": []}

from json import dumps, loads


def find_key_differences(lst1, lst2, keys_to_compare):
    # Convert lists of dictionaries to sets of their JSON representations
    set1 = dicts_to_set(lst1, keys_to_compare)
    print(set1)
    set2 = dicts_to_set(lst2, keys_to_compare)
    print(set2)

    # Deserialize elements in set1 that are not in set2
    return [loads(x) for x in set1.difference(set2)]


def dicts_to_set(lst, keys_to_compare):
    '''
    Convert a list of dictionaries to a set of their JSON representations,
    considering only specified keys for comparison.
    '''
    return set(dumps({k: x[k] for k in keys_to_compare}, sort_keys=True) for x in lst)


# Example usage:

#
# keys_to_compare = ['longitude', 'latitude']
# differences = find_key_differences(requests_positions["positions"], response["data"], keys_to_compare)
#
# print("Differences based on specified keys:")
# for diff in differences:
#     print(diff)


def find_unmatch_lat_long(request_points: list, response_points: list):
    """
    This function will return the unmatch points lat long value that return from response content
    after validation
    :param request_points: request body points lat long values
    :param response_points: response points lat long values
    :return:
    list of unmatch lat long values
    """
    keys_to_compare = ['longitude', 'latitude']
    validate_json_array_length(json_array=response_points, expected_length=len(request_points))
    request_points_set = set(json.dumps({k: x[k] for k in keys_to_compare}, sort_keys=True) for x in request_points)
    response_points_set = set(json.dumps({k: x[k] for k in keys_to_compare}, sort_keys=True) for x in response_points)
    return [json.loads(x) for x in response_points_set.difference(request_points_set)]


# print(find_unmatch_lat_long(request_points=requests_positions["positions"], response_points=response["data"]))
def find_null_points(response_content: dict):
    """
    This function will return
    :param response_content:
    :return:
    """
    try:
        heights_list = response_content.get("data")
    except Exception as e:
        return e
    if len(heights_list) != 0:
        null_points = [
            item for item in heights_list if item.get("height") is None
        ]
        return null_points

print("check the null function")
print(find_null_points(response_content=response))