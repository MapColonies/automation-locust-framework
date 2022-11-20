import math
from math import floor
from typing import Optional
from typing import Tuple

import common.config


def zoom_level_convertor(deg_value: float) -> Optional[int]:
    """

    :param deg_value: float number that presents the resolution deg
    :return: zoom level value : int
    """
    zoom_level = math.floor(math.log2(180 / (deg_value * 256)))
    return zoom_level


class Range:
    def __init__(self, min_val: int, max_val: int):
        self.min_val = min_val
        self.max_val = max_val
        self.range = self.get_range_value()

    def get_range_value(self):
        return self.min_val, self.max_val


class MapproxyLayer:
    def __init__(self, layer_id: str, zoom: int, product_bbox: list):
        self.layer_id = layer_id
        self.zoom = zoom
        self.bbox = product_bbox

    @property
    def get_layer_id(self) -> str:
        return self.layer_id

    @property
    def min_x_deg(self) -> float:
        return self.bbox[0]

    @property
    def min_y_deg(self) -> float:
        return self.bbox[1]

    @property
    def max_x_deg(self) -> float:
        return self.bbox[2]

    @property
    def max_y_deg(self) -> float:
        return self.bbox[3]

    @property
    def zoom_level(self) -> int:
        return self.zoom

    @property
    def deg_per_tile(self):
        return self.get_deg_per_tile(zoom_level=self.zoom_level)

    def get_x_tile_ranges(self) -> Tuple[int, int]:
        min_tile_x = floor((self.min_x_deg + 180) / self.deg_per_tile)
        max_tile_x = floor((self.max_x_deg + 180) / self.deg_per_tile) + 1
        return Range(min_tile_x, max_tile_x).get_range_value()

    def get_y_tile_ranges(self) -> Tuple[int, int]:
        min_tile_y = (
            pow(2, self.zoom_level)
            - floor((self.max_y_deg + 90) / self.deg_per_tile)
            - 1
        )
        max_tile_y = pow(2, self.zoom_level) - floor(
            (self.min_y_deg + 90) / self.deg_per_tile
        )
        return Range(min_tile_y, max_tile_y).get_range_value()

    def get_zoom_range(self) -> Optional[Tuple[int, int]]:
        # zoom_level = zoom_level_convertor(deg_value=self.zoom_deg)
        # if zoom_level:
        return Range(0, self.zoom_level).get_range_value()
        # return None

    def get_deg_per_tile(self, zoom_level: int):
        deg_per_tile = 180 / pow(2, zoom_level)
        return deg_per_tile


# usage example
# x = MapproxyLayer(
#     "shay_165",
#     4,
#     [35.0884731109971, 31.7732841960024, 35.172258148995, 31.828506152999],
# )
# print(f"x_tile: {x.get_x_tile_ranges()}")
# print(f"y_tile: {x.get_y_tile_ranges()}")
# print(f"zoom: {x.get_zoom_range()}")
