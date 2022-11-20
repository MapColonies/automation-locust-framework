from math import floor


def get_resolution_by_zoom_lavel(zoom_level: int) -> float:
    res = 180 / (pow(2, zoom_level)) / 256
    return res


def get_max_x_and_y_range(zoom_level, min_x, max_x, min_y, max_y):
    res = 180 / (pow(2, zoom_level)) / 256
    min_x_snap = floor(min_x / res) * res
    max_x_snap = floor(max_x / res) * res
    if min_x_snap != 180:
        min_x_snap += res
    if zoom_level == 0:
        min_y_snap = -90
        max_y_snap = 90
    else:
        min_y_snap = floor(min_y / res) * res
        max_y_snap = floor(max_y / res) * res
    if max_y_snap != 90:
        max_y_snap += res
    tiles_size_deg = res * 256
    min_y_tile = -min_y_snap
    max_y_tile = -max_y_snap
    min_x_tile = (min_x_snap / tiles_size_deg) + pow(2, zoom_level)
    max_x_tile = (max_x_snap / tiles_size_deg) + pow(2, zoom_level)

    return (min_y_tile, max_y_tile), (min_x_tile, max_x_tile)


# print(get_max_x_and_y_range(zoom_level=4, min_x=35.024411528661574, max_x=32.79419004139809, min_y=35.37597717328861, max_y=32.947998391903226))


def convert_tile_to_bbox():
    max_lan = 180
    max_lat = 90


deg_per_tile = 0.001373
zoom_level = 4
# minx_deg, miny_deg , maxx_deg , maxy_deg, zoom_level
# min_tile_x = floor((minx_deg+180)/deg_per_tile,1)
# max_tile_x = floor((maxx_deg+180)/deg_per_tile,1)+1
# min_tile_y = power(2,zoom_level) - floor((maxy_deg+90)/deg_per_tile,1) -1
# max_tile_y = power(2,zoom_level) - floor((miny_deg+90)/deg_per_tile,1)
def get_min_tile_x(min_x_deg):
    min_tile_x = floor((min_x_deg + 180) / deg_per_tile)
    return min_tile_x


def get_max_tile_x(max_x_deg):
    max_tile_x = floor((max_x_deg + 180) / deg_per_tile) + 1
    return max_tile_x


def get_min_tile_y(max_y_deg):
    min_tile_y = pow(2, zoom_level) - floor((max_y_deg + 90) / deg_per_tile) - 1
    return min_tile_y


print(get_min_tile_x(35.024411528661574))
print(get_max_tile_x(32.79419004139809))
print(get_min_tile_y(32.947998391903226))
