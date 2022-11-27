from itertools import product
from typing import Iterable

from config.config import config_obj


class WMTSIterator:
    "WMTSIterator - with range"

    def __init__(self, range_: range):
        self.points = iter(range_)
        self.range = range_

    def __next__(self) -> Iterable[int]:
        try:
            return next(self.points)
        except StopIteration:
            self.points = iter(self.range)
            return next(self.points)


def wmts_url_builder(x_val, y_val, zoom_val):
    """
    This method build the url of given tile parameters
    :return:
    wmts_url: url of the given layer's tile
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


def create_tiles_url_order(zoom_ranges, x_ranges, y_ranges):
    """
    This method create possible tiles order based on range's value
    :param zoom_ranges: zoom ranges value
    :param x_ranges: x ranges value
    :param y_ranges: y ranges value"""
    x_values = [*range(x_ranges[0], x_ranges[1] + 1)]
    y_values = [*range(y_ranges[0], y_ranges[1] + 1)]
    zoom_values = [*range(zoom_ranges[0], zoom_ranges[1] + 1)]
    print(list(product(zoom_values, y_values, x_values)))
    print(len(list(product(zoom_values, y_values, x_values))))
    return list(product(zoom_values, y_values, x_values))
