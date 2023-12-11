import json
import random
from typing import List, Tuple

from shapely.geometry import Point, Polygon

poly = [
    (37.75850848099701, -122.50833008408812),
    (37.75911919711413, -122.49648544907835),
    (37.751620611284935, -122.4937388670471),
    (37.74863453749236, -122.50742886185911),
]


def polygon_random_points(
        polygon: List[Tuple[float, float]], num_points: int
) -> List[Tuple[float, float]]:
    """
    This function will generate points by a given polygon
    :param polygon: Polygon coordinates of the desired points zone
    :param num_points: points amount to be generated
    :return:
    list of lat long values
    """
    polygon = Polygon(polygon)
    min_x, min_y, max_x, max_y = polygon.bounds
    points = []
    while len(points) < num_points:
        random_point = Point(
            [random.uniform(min_x, max_x), random.uniform(min_y, max_y)]
        )
        if random_point.within(polygon):
            point_val = (float(random_point.x), float(random_point.y))
            points.append(point_val)
    return points


def generate_points_request(
        points_amount: int,
        polygon: List[Tuple[float, float]],
        exclude_fields: bool,
        product_type: str = "MIXED",
):
    """
    This function will generate request body for user
    :param points_amount: point amount to be generated
    :param polygon: Polygon object of the desired points zone
    :param exclude_fields: indicate if the excludeFields will be empty or not
    :param product_type: [ DSM, DTM, MIXED ]
    :return:
    request body
    """
    points_data = polygon_random_points(polygon=polygon, num_points=points_amount)
    points_list = []
    for points_cor in points_data:
        points = {"longitude": points_cor[0], "latitude": points_cor[1]}
        points_list.append(points)
    if exclude_fields:
        request_body = json.dumps(
            {"positions": points_list, "productType": product_type}
        )
        return request_body
    else:
        request_body = json.dumps(
            {
                "positions": points_list,
                "productType": product_type,
            }
        )
        return request_body


def custom_sorting_key(item):
    # Extract the lower bound of the range from the key
    lower_bound = int(item[0].split(",")[0].strip("("))
    return lower_bound


poly1 = [
    (34.9718214942001, 32.80423530554715),
    (34.9718214942001, 32.756206767248315),
    (35.06487372085749, 32.756206767248315),
    (35.06487372085749, 32.80423530554715),
    (34.9718214942001, 32.80423530554715),
]


# print(polygon_random_points(num_points=3, polygon=poly1))
print(generate_points_request(points_amount=3, polygon=poly1, exclude_fields=True))
#
# x = [(34.99329017908319, 32.75730973158232), (34.99798221083507, 32.79931519606793),
#      (35.00240318612141, 32.7935654102479), (35.04743080042179, 32.795414543794415)]
# dict1 = {"positions": [{"longitude": 34.99329017908319, "latitude": 32.75730973158232},
#                        {"longitude": 34.99798221083507, "latitude": 32.79931519606793},
#                        {"longitude": 35.00240318612141, "latitude": 32.7935654102479},
#                        {"longitude": 35.01469671603069, "latitude": 32.78338486794766},
#                        {"longitude": 35.04743080042179, "latitude": 32.795414543794415}], "productType": "MIXED",
#          "excludeFields": []}


def find_keys_by_values(input_dict, value_tuples, keys):
    result = {}
    for key1, key2 in keys:
        if key1 in input_dict and key2 in input_dict:
            value_tuple = (input_dict[key1], input_dict[key2])
            print(value_tuple)
            if value_tuple in value_tuples:
                result[key1] = input_dict[key1]
                result[key2] = input_dict[key2]
    return result


# print(find_keys_by_values(input_dict=dict1, value_tuples=x, keys=[("longitude", "latitude")]))
#
# x =[(34.99329017908319, 32.75730973158232), (34.99798221083507, 32.79931519606793),
#      (35.00240318612141, 32.7935654102479), (35.04743080042179, 32.795414543794415)]
# dict1 = {"check": [{"key1": 34.99329017908319, "key2": 32.75730973158232},
#                    {"key1": 34.99798221083507, "key2": 32.79931519606793},
#                    {"key1": 35.00240318612141, "key2": 32.7935654102479},
#                    {"key1": 35.01469671603069, "key2": 32.78338486794766},
#                    {"key1": 35.04743080042179, "key2": 32.795414543794415}], "field1": "MIXED",
#          "field2": []}
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
