import json

import numpy as np
import random
from shapely.geometry import Polygon, Point

poly = [(37.75850848099701, -122.50833008408812), (37.75911919711413, -122.49648544907835),
                (37.751620611284935, -122.4937388670471), (37.74863453749236, -122.50742886185911)]


def polygon_random_points(polygon: list, num_points: int) -> list:
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
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if random_point.within(polygon):
            point_val = (float(random_point.x), float(random_point.y))
            points.append(point_val)
    return points


def generate_points_request(points_amount: int, poly: list, payload_flag: bool, product_type="MIXED"):
    """
    This function will generate request body for user
    :param points_amount: point amount to be generated
    :param poly: Polygon object of the desired points zone
    :param payload_flag: indicate if the excludeFields will be empty or not
    :param product_type: [ DSM, DTM, MIXED ]
    :return:
    request body
    """
    points_data = polygon_random_points(polygon=poly, num_points=points_amount)
    points_list = []
    for points_cor in points_data:
        points = {
            "longitude": points_cor[0],
            "latitude": points_cor[1]
        }
        points_list.append(points)
    if payload_flag:
        request_body = json.dumps({"positions": points_list, "productType": product_type, "excludeFields": []})
        return request_body
    else:
        request_body = json.dumps({"positions": points_list, "productType": product_type,
                                   "excludeFields": ["productType", "updateDate", "resolutionMeter"]})
        return request_body
