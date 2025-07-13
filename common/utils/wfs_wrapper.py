import json
import math

import requests
import random
from lxml import etree
from typing import List, Tuple
from shapely.geometry import shape, Polygon, MultiPolygon, Point, box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
import geojson
import numpy as np

from common.config.config import config_obj
from common.utils.requests_logger import log_request, insert_request_log


class WFSClient:
    """
    wrapper for all WFS operations
    """

    def __init__(self, base_url, version, token, output_format="application/json"):
        self.session = requests.session()
        self.base_url = base_url
        self.version = version
        self.token = token
        self.output_format = output_format

    def get_capabilities(self):
        """
        The GetCapabilities operation is a request to a WFS server for a list of the operations and services,
         or capabilities, supported by that server.
        """
        params = {
            "service": "WFS",
            "request": "GetCapabilities",
            "version": self.version,
            "token": self.token
        }
        response = self.session.get(self.base_url, params=params)
        response.raise_for_status()
        return response

    def describe_feature_type(self, type_name):
        """
        DescribeFeatureType requests information about an individual feature type before requesting the actual data.
        Specifically, the operation will request a list of features and attributes for the given feature type,
        or list the feature types available.
        """
        params = {
            "service": "WFS",
            "version": self.version,
            "request": "DescribeFeatureType",
            "typeNames": type_name,
            "token": self.token,
            "outputFormat": self.output_format

        }
        response = self.session.get(self.base_url, params=params)
        response.raise_for_status()
        return response

    def get_feature(self, logic_operator=None, filters=None, request_params=None):
        """
        The GetFeature operation returns a selection of features from the data source.

        :param logic_operator: "And" or "Or" for combining filters (used only if filters is a list).
        :param filters: Either a list of attribute filter tuples, or a full XML string (e.g., Intersects filter).
        :param request_params: Additional query parameters.
        """
        if isinstance(filters, str):
            params = {
                "service": "WFS",
                "request": "GetFeature",
                "version": self.version,
                "outputFormat": self.output_format,
                "token": self.token
            }
            # Full XML body provided (e.g., Intersects request)
            headers = {"Content-Type": "application/xml"}
            response = self.session.post(self.base_url, data=filters, params=params, headers=headers)
            log_request(method="POST", url=self.base_url, params=params, body=filters, headers=headers)




        else:
            # Attribute filter mode (fallback to old behavior)
            params = {
                "service": "WFS",
                "request": "GetFeature",
                "version": self.version,
                "outputFormat": self.output_format,
                "token": self.token
            }
            if request_params:
                params.update(request_params)

            if filters:
                headers = {"Content-Type": "application/xml"}
                filter_xml = self.create_wfs_filter(filters, logic_operator)
                response = self.session.post(self.base_url, params=params, data=filter_xml, headers=headers)
                print("hi1")
                log_request(method="POST", url=self.base_url, params=params, body=filters, headers=headers)

            else:
                response = self.session.get(self.base_url, params=params)
                print(f"status_code: {response.status_code}")
                print("hi2")
                headers = {"Content-Type": "application/xml"}
                log_request(method="POST", url=self.base_url, params=params, body=filters, headers=headers)

        response.raise_for_status()

        return response

    def transaction(self, transaction_xml):
        headers = {"Content-Type": "application/xml"}
        response = self.session.post(self.base_url, data=transaction_xml, headers=headers)
        response.raise_for_status()
        return response

    @staticmethod
    def create_wfs_filter(
            filters: List[Tuple[str, str]],
            logic_operator: str = "And",
            ogc_version: str = "1.1.0"
    ) -> str:
        """
        Generates a WFS filter XML for a GetFeature request with multiple equality filters.

        :param filters: List of (property_name, literal_value) tuples.
        :param logic_operator: Logical operator to combine filters: "And" or "Or".
        :param ogc_version: OGC version ("1.1.0" or "2.0").
        :return: XML string of the filter.
        """
        ogc_ns = {
            '1.1.0': 'http://www.opengis.net/ogc',
            '2.0': 'http://www.opengis.net/fes/2.0'
        }

        ns_uri = ogc_ns.get(ogc_version, ogc_ns['1.1.0'])

        ogc = etree.Element("{%s}Filter" % ns_uri)

        if len(filters) == 1:
            container = ogc
        else:
            container = etree.SubElement(ogc, "{%s}%s" % (ns_uri, logic_operator))

        for prop, value in filters:
            comp = etree.SubElement(container, "{%s}PropertyIsEqualTo" % ns_uri)
            prop_elem = etree.SubElement(comp, "{%s}PropertyName" % ns_uri)
            prop_elem.text = prop
            val_elem = etree.SubElement(comp, "{%s}Literal" % ns_uri)
            val_elem.text = value

        return etree.tostring(ogc, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode("utf-8")

    @staticmethod
    def create_intersects_filter(pos_list: List[float], type_name: str) -> str:
        """
        Generates a full WFS GetFeature XML body with an Intersects filter using a gml:Polygon.

        :param pos_list: List of coordinates in [x1, y1, x2, y2, ..., xn, yn] format.
        :param type_name: Feature type name to query.
        :return: XML string of the GetFeature request.
        """
        # Namespaces
        NSMAP = {
            'wfs': "http://www.opengis.net/wfs/2.0",
            'fes': "http://www.opengis.net/fes/2.0",
            'gml': "http://www.opengis.net/gml/3.2",
            'xsi': "http://www.w3.org/2001/XMLSchema-instance",
            'my': "http://www.someserver.com/my"
        }

        # Root element
        root = etree.Element(
            "{http://www.opengis.net/wfs/2.0}GetFeature",
            nsmap=NSMAP,
            service="WFS",
            version="2.0.0",
            attrib={
                "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation":
                    "http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd"
            }
        )

        # wfs:Query
        query = etree.SubElement(root, "{http://www.opengis.net/wfs/2.0}Query", typeNames=type_name)

        # fes:Filter
        filter_elem = etree.SubElement(query, "{http://www.opengis.net/fes/2.0}Filter")

        # fes:Intersects
        intersects = etree.SubElement(filter_elem, "{http://www.opengis.net/fes/2.0}Intersects")

        # fes:ValueReference
        value_ref = etree.SubElement(intersects, "{http://www.opengis.net/fes/2.0}ValueReference")
        value_ref.text = "geom"

        # gml:Polygon
        polygon = etree.SubElement(
            intersects,
            "{http://www.opengis.net/gml/3.2}Polygon",
            srsName="EPSG:4326"
        )
        exterior = etree.SubElement(polygon, "{http://www.opengis.net/gml/3.2}exterior")
        linear_ring = etree.SubElement(exterior, "{http://www.opengis.net/gml/3.2}LinearRing")
        pos_list_elem = etree.SubElement(linear_ring, "{http://www.opengis.net/gml/3.2}posList")

        # Format posList as space-separated string
        pos_list_elem.text = " ".join(f"{x:.14f}" for x in pos_list)

        return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode('utf-8')

    @staticmethod
    def create_wfs_point_dwithin_filter_body(
            point: str,
            distance: float,
            type_name: str = "sf:archsites",
            srs_name: str = "http://www.opengis.net/gml/srs/epsg.xml#26713",
            property_name: str = "the_geom"
    ) -> str:
        """
        Creates a WFS 1.0.0 GetFeature request body using a DWithin spatial filter with a GML point.

        :param point: Coordinate string in format "x,y" (e.g., "593250,4923867")
        :param distance: Distance in meters
        :param type_name: Feature type name
        :param srs_name: Spatial reference system URI
        :param property_name: Geometry field name
        :return: XML string
        """
        NSMAP = {
            "wfs": "http://www.opengis.net/wfs",
            "ogc": "http://www.opengis.net/ogc",
            "gml": "http://www.opengis.net/gml",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }

        root = etree.Element(
            "{http://www.opengis.net/wfs}GetFeature",
            nsmap=NSMAP,
            service="WFS",
            version="1.0.0",
            outputFormat="application/json",
            attrib={
                "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation":
                    "http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/WFS-basic.xsd"
            }
        )

        query = etree.SubElement(root, "{http://www.opengis.net/wfs}Query", typeName=type_name)
        filter_elem = etree.SubElement(query, "{http://www.opengis.net/ogc}Filter")
        dwithin = etree.SubElement(filter_elem, "{http://www.opengis.net/ogc}DWithin")

        prop_elem = etree.SubElement(dwithin, "{http://www.opengis.net/ogc}PropertyName")
        prop_elem.text = property_name

        gml_point = etree.SubElement(dwithin, "{http://www.opengis.net/gml}Point", srsName=srs_name)
        coordinates = etree.SubElement(gml_point, "{http://www.opengis.net/gml}coordinates")
        coordinates.text = point

        distance_elem = etree.SubElement(dwithin, "{http://www.opengis.net/ogc}Distance", units="meter")
        distance_elem.text = str(distance)

        return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode("utf-8")

    @staticmethod
    def create_attribute_filter(attribute: str, value: str, type_names: str) -> str:
        """
        Create a WFS GetFeature request body for an attribute-based query.

        :param attribute: The name of the attribute (e.g., 'sensors').
        :param value: The value to match (e.g., 'shay').
        :param type_names: The WFS feature type name.
        :return: XML string of the full GetFeature request body.
        """
        NSMAP = {
            "wfs": "http://www.opengis.net/wfs/2.0",
            "fes": "http://www.opengis.net/fes/2.0",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "my": "http://www.someserver.com/my"
        }

        root = etree.Element(
            "{http://www.opengis.net/wfs/2.0}GetFeature",
            service="WFS",
            version="2.0.0",
            nsmap=NSMAP
        )
        root.set(
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation",
            "http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd"
        )

        query = etree.SubElement(
            root,
            "{http://www.opengis.net/wfs/2.0}Query",
            typeNames=type_names
        )

        filter_elem = etree.SubElement(query, "{http://www.opengis.net/fes/2.0}Filter")
        comparison = etree.SubElement(filter_elem, "{http://www.opengis.net/fes/2.0}PropertyIsEqualTo")

        val_ref = etree.SubElement(comparison, "{http://www.opengis.net/fes/2.0}ValueReference")
        val_ref.text = attribute

        literal = etree.SubElement(comparison, "{http://www.opengis.net/fes/2.0}Literal")
        literal.text = str(value)

        return etree.tostring(root, pretty_print=True, encoding="UTF-8", xml_declaration=True).decode("utf-8")


class GeoGenerator:
    """
    This class will provide geo utils to test data generation
    """

    def __init__(self, ROI_PATH):
        self.ROI = ROI_PATH
        self.geometry = self._load_and_merge_geometry()

    def _load_and_merge_geometry(self):
        """
        Load and merge all features in the GeoJSON into a single geometry (Polygon or MultiPolygon).
        """
        with open(self.ROI, 'r') as f:
            geojson_data = json.load(f)

        if "features" not in geojson_data:
            raise ValueError("GeoJSON must contain 'features'.")

        geometries = [shape(feature["geometry"]) for feature in geojson_data["features"]]
        merged_geom = unary_union(geometries)

        if not isinstance(merged_geom, (Polygon, MultiPolygon)):
            raise ValueError("GeoJSON must contain Polygon or MultiPolygon geometries.")

        return merged_geom

    def get_random_point(self):
        """
        Get a random Point within a polygon from a GeoJSON geometry or feature collection.
        :return: A Shapely Point object within a randomly selected polygon.
        """
        if isinstance(self.ROI, str):
            with open(self.ROI, 'r') as file:
                geojson_content = json.load(file)
        else:
            raise ValueError(f"Invalid ROI path value - {self.ROI}")

        # Extract all polygons
        polygons = []

        features = geojson_content.get("features",
                                       [geojson_content])  # handles both FeatureCollection and single Feature

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
                return list(random_point.coords[0])

        raise RuntimeError("Unable to find a point inside any polygon.")

    def get_random_bbox(self, min_width=0.01, max_width=0.5, min_height=0.01, max_height=0.5):
        """
        Generate a random bounding box within the bounds of a GeoJSON containing polygons.

        :param min_width: Minimum width of the random bbox.
        :param max_width: Maximum width of the random bbox.
        :param min_height: Minimum height of the random bbox.
        :param max_height: Maximum height of the random bbox.
        :return: List of bbox values [minx, miny, maxx, maxy].
        """
        if isinstance(self.ROI, str):
            with open(self.ROI, 'r') as file:
                geojson_content = json.load(file)
        else:
            raise ValueError(f"Invalid ROI path value - {self.ROI}")

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

    def generate_random_polygon(self, vertex_count):
        """
        Generates a random simple (non-self-intersecting) polygon within a GeoJSON-defined area.

        Args:
            vertex_count (int): Number of vertices for the generated polygon (minimum 4 for a closed polygon).

        Returns:
            list: A list of floats representing the polygon: [lon1, lat1, lon2, lat2, ..., lonN, latN]
        """
        if vertex_count < 4:
            raise ValueError("vertex_count must be at least 4 (including closing vertex)")

        if isinstance(self.ROI, str):
            with open(self.ROI, 'r') as file:
                geojson_obj = json.load(file)
        else:
            raise ValueError(f"Invalid ROI path value - {self.ROI}")

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

            # Generate points with random angles, but sort them to avoid self-intersection
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


# x = GeoGenerator(ROI_PATH="/home/shayavr/Desktop/git/automation-locust-framework/test_data/roi.geojson")
# print(x.generate_random_polygon(vertex_count=4))