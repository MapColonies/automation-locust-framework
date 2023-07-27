from math import floor, pow

EQUATOR_DEGREES = 180
MAX_LATITUDE = 90
TILE_SIZE = 256
TILE_DEGREE = 0.001373
ZOOM_LEVEL = 4


def calculate_resolution(zoom_level: int) -> float:
    """Calculate the resolution based on the zoom level."""
    return EQUATOR_DEGREES / pow(2, zoom_level) / TILE_SIZE


def get_normalized_coordinate_range(range_zoom_level, min_x, max_x, min_y, max_y):
    """Calculate the min and max tiles for x and y."""
    res = calculate_resolution(range_zoom_level)
    min_x_snap = floor(min_x / res) * res
    max_x_snap = floor(max_x / res) * res

    if min_x_snap != EQUATOR_DEGREES:
        min_x_snap += res

    if range_zoom_level == 0:
        min_y_snap = -MAX_LATITUDE
        max_y_snap = MAX_LATITUDE
    else:
        min_y_snap = floor(min_y / res) * res
        max_y_snap = floor(max_y / res) * res

    if max_y_snap != MAX_LATITUDE:
        max_y_snap += res

    tiles_size_deg = res * TILE_SIZE
    min_y_tile = -min_y_snap
    max_y_tile = -max_y_snap
    min_x_tile = (min_x_snap / tiles_size_deg) + pow(2, range_zoom_level)
    max_x_tile = (max_x_snap / tiles_size_deg) + pow(2, range_zoom_level)

    return {
        "min_y_tile": min_y_tile,
        "max_y_tile": max_y_tile,
        "min_x_tile": min_x_tile,
        "max_x_tile": max_x_tile,
    }


def calculate_tile_x(deg, add_one=False):
    """Calculate the tile number in the x direction based on degrees."""
    tile_x = floor((deg + EQUATOR_DEGREES) / TILE_DEGREE)
    return tile_x + 1 if add_one else tile_x


def calculate_min_tile_y(max_y_deg):
    """Calculate the minimum tile number in the y direction based on max degrees."""
    return pow(2, ZOOM_LEVEL) - floor((max_y_deg + MAX_LATITUDE) / TILE_DEGREE) - 1
