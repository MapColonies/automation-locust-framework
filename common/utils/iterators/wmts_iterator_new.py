from itertools import product
from typing import List, Tuple

from common.config.config import config_obj

# ToDo seprate to class if needed


# class WMTSIterator:
#     """WMTSIterator - with range"""
#
#     def __init__(self, range_: range):
#         self.points = iter(range_)
#         self.range = range_
#
#     def __next__(self) -> Iterable[int]:
#         try:
#             return next(self.points)
#         except StopIteration:
#             self.points = iter(self.range)
#             return next(self.points)
def wmts_url_builder(x_val: int, y_val: int, zoom_val: int) -> str:
    """
    This method builds the URL of given tile parameters
    :param x_val: x coordinate
    :param y_val: y coordinate
    :param zoom_val: zoom level
    :return: URL of the given layer's tile
    """
    wmts_url = (
        f"/{config_obj['wmts'].LAYER_TYPE}/"
        f"{config_obj['wmts'].LAYER_NAME}/"
        f"{config_obj['wmts'].GRID_NAME}/"
        f"{x_val}/{y_val}/"
        f"{zoom_val}{config_obj['wmts'].IMAGE_FORMAT}"
        f"?token={config_obj['wmts'].TOKEN}"
    )
    return wmts_url


def create_tiles_url_order(
    zoom_ranges: Tuple[int, int], x_ranges: Tuple[int, int], y_ranges: Tuple[int, int]
) -> List[Tuple[int, int, int]]:
    """
    This method creates possible tiles order based on range's value
    :param zoom_ranges: zoom ranges value
    :param x_ranges: x ranges value
    :param y_ranges: y ranges value
    :return: List of tuples containing zoom, y and x values
    """
    x_values = range(x_ranges[0], x_ranges[1] + 1)
    y_values = range(y_ranges[0], y_ranges[1] + 1)
    zoom_values = range(zoom_ranges[0], zoom_ranges[1] + 1)
    tile_orders = list(product(zoom_values, y_values, x_values))
    print(tile_orders)
    print(len(tile_orders))
    return tile_orders
