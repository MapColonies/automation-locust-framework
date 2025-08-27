
import json
import math
import random
from shapely.geometry import shape, Point, Polygon, MultiPolygon
from shapely.ops import unary_union
from common.config.config import WfsConfig

def generate_random_polygon(geojson_path: str, vertex_count: int) -> list:
    """
    Generates a random simple (non-self-intersecting) polygon within a GeoJSON-defined area.

    Args:
        geojson_path (str): Path to the GeoJSON file containing the area of interest.
        vertex_count (int): Number of vertices for the generated polygon (minimum 4 for a closed polygon).

    Returns:
        list: A list of floats representing the polygon: [lon1, lat1, lon2, lat2, ..., lonN, latN]
    """
    if vertex_count < 4:
        raise ValueError("vertex_count must be at least 4 (including closing vertex)")

    with open(geojson_path, 'r') as file:
        geojson_obj = json.load(file)

    geom = shape(geojson_obj['features'][0]['geometry'])

    if isinstance(geom, MultiPolygon):
        geom = unary_union(geom)

    minx, miny, maxx, maxy = geom.bounds

    for _ in range(1000):  # max attempts
        cx = random.uniform(minx, maxx)
        cy = random.uniform(miny, maxy)
        center = Point(cx, cy)

        if not geom.contains(center):
            continue

        max_radius = min(maxx - minx, maxy - miny) * 0.01
        radius = random.uniform(max_radius * 0.5, max_radius)

        # Generate points with random angles, sort them to avoid self-intersection
        angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(vertex_count - 1)])
        coords = [
            (
                cx + radius * math.cos(angle),
                cy + radius * math.sin(angle)
            )
            for angle in angles
        ]
        coords.append(coords[0])  # Close the polygon

        candidate_poly = Polygon(coords)
        if geom.contains(candidate_poly):
            return [round(coord, 14) for point in coords for coord in point]

    return None



print(generate_random_polygon(geojson_path=WfsConfig.ROI_PATH,vertex_count=5))