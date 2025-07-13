import json
import random
from shapely.geometry import shape, box
from shapely.ops import unary_union

def get_random_bbox(min_width=1, max_width=100, min_height=1, max_height=100):
    """
    Generate a random bounding box within the bounds of a GeoJSON containing polygons.

    :param min_width: Minimum width of the random bbox.
    :param max_width: Maximum width of the random bbox.
    :param min_height: Minimum height of the random bbox.
    :param max_height: Maximum height of the random bbox.
    :return: List of bbox values [minx, miny, maxx, maxy].
    """
    with open("/home/shayavr/Desktop/git/automation-locust-framework/test_data/roi.geojson", 'r') as file:
        geojson_content = json.load(file)


    geometries = [shape(feature["geometry"]) for feature in geojson_content["features"]]
    merged_geom = unary_union(geometries)
    minx, miny, maxx, maxy = merged_geom.bounds

    for _ in range(100):
        # Random bbox size
        bbox_width = random.uniform(min_width, min(max_width, maxx - minx))
        bbox_height = random.uniform(min_height, min(max_height, maxy - miny))

        # Restrict origin so bbox stays inside bounds
        x_range = maxx - minx - bbox_width
        y_range = maxy - miny - bbox_height

        if x_range <= 0 or y_range <= 0:
            continue  # Try again with different size

        rand_minx = random.uniform(minx, minx + x_range)
        rand_miny = random.uniform(miny, miny + y_range)
        candidate_bbox = box(rand_minx, rand_miny, rand_minx + bbox_width, rand_miny + bbox_height)

        if merged_geom.intersects(candidate_bbox):
            return ", ".join(
                str(x) for x in [rand_minx, rand_miny, rand_minx + bbox_width, rand_miny + bbox_height])

    raise RuntimeError("Failed to generate a valid random bbox within geometry after 100 attempts.")


print(get_random_bbox())