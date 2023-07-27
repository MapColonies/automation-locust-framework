from math import floor, pow
from typing import Tuple

DEGREES_PER_TILE = 180
TILES_PER_ZOOM = 256
DEGREES_FOR_X = 180
DEGREES_FOR_Y = 90
RANGE_POWER = 2


class Range:
    def __init__(self, min_val: int, max_val: int):
        self.min_val = min_val
        self.max_val = max_val


class MapproxyLayer:
    def __init__(self, layer_id: str, zoom: int, product_bbox: list):
        self.layer_id = layer_id
        self.zoom = zoom
        self.bbox = product_bbox

    @property
    def layer_id(self) -> str:
        return self._layer_id

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
        min_tile_x = floor((self.min_x_deg + DEGREES_FOR_X) / self.deg_per_tile)
        max_tile_x = floor((self.max_x_deg + DEGREES_FOR_X) / self.deg_per_tile) + 1
        return Range(min_tile_x, max_tile_x)

    def get_y_tile_ranges(self) -> Tuple[int, int]:
        min_tile_y = (
            pow(RANGE_POWER, self.zoom_level)
            - floor((self.max_y_deg + DEGREES_FOR_Y) / self.deg_per_tile)
            - 1
        )
        max_tile_y = pow(RANGE_POWER, self.zoom_level) - floor(
            (self.min_y_deg + DEGREES_FOR_Y) / self.deg_per_tile
        )
        return Range(min_tile_y, max_tile_y)

    def get_zoom_range(self) -> Tuple[int, int]:
        return Range(0, self.zoom_level)

    def get_deg_per_tile(self, zoom_level: int):
        deg_per_tile = DEGREES_PER_TILE / pow(RANGE_POWER, zoom_level)
        return deg_per_tile
