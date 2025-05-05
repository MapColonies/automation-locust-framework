import random
import json
from shapely.geometry import shape, Polygon, MultiPolygon, Point


def get_random_point_from_geojson(geojson_content):
    """
    Get a random Point within a polygon from a GeoJSON geometry or feature collection.

    :param geojson_content: A dict or JSON string of the GeoJSON.
    :return: A Shapely Point object within a randomly selected polygon.
    """
    if isinstance(geojson_content, str):
        geojson_content = json.loads(geojson_content)

    # Extract all polygons
    polygons = []

    features = geojson_content.get("features", [geojson_content])  # handles both FeatureCollection and single Feature

    for feature in features:
        geom = feature.get("geometry", feature)  # handle raw geometry or full feature
        shapely_geom = shape(geom)
        if isinstance(shapely_geom, Polygon):
            polygons.append(shapely_geom)
        elif isinstance(shapely_geom, MultiPolygon):
            polygons.extend(list(shapely_geom.geoms))

    if not polygons:
        raise ValueError("No polygons found in the GeoJSON input.")

    # Randomly choose a polygon
    selected_polygon = random.choice(polygons)

    # Randomly pick a point inside the selected polygon
    minx, miny, maxx, maxy = selected_polygon.bounds
    for _ in range(1000):  # Limit attempts
        random_point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if selected_polygon.contains(random_point):
            return random_point

    raise RuntimeError("Unable to find a point inside any polygon.")


