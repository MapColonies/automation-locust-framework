import json
import requests
import random
from lxml import etree
from typing import List, Tuple
from shapely.geometry import shape, Polygon, MultiPolygon, Point


class WFSClient:
    """
    wrapper for all WFS operations
    """

    def __init__(self, base_url, version, token, output_format="application/json"):
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
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.text

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
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json() if self.output_format == "application/json" else response.text

    def get_feature(self, type_name, logic_operator=None, filters=None, request_params=None):
        """
        The GetFeature operation returns a selection of features from the data source.
        """
        params = {
            "service": "WFS",
            "request": "GetFeature",
            "version": self.version,
            "typeName": type_name,
            "outputFormat": self.output_format,
            "token": self.token
        }
        if request_params:
            params.update(request_params)

        if filter:
            headers = {"Content-Type": "application/xml"}
            filter_xml = self.create_wfs_filter(filters, logic_operator)
            response = requests.post(self.base_url, params=params, data=filter_xml, headers=headers)
        else:
            response = requests.get(self.base_url, params=params)

        response.raise_for_status()
        return response.json() if self.output_format == "application/json" else response.text

    def transaction(self, transaction_xml):
        headers = {"Content-Type": "application/xml"}
        response = requests.post(self.base_url, data=transaction_xml, headers=headers)
        response.raise_for_status()
        return response.text

    def create_wfs_filter(self,
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


class GeoGenerator:
    """
    This class will provide geo utils to test data generation
    """

    def __init__(self, ROI):
        self.ROI = ROI

    def get_random_bbox(self):
        """
        Get a random Point within a polygon from a GeoJSON geometry or feature collection.

        :param geojson_content: A dict or JSON string of the GeoJSON.
        :return: A Shapely Point object within a randomly selected polygon.
        """
        if isinstance(self.ROI, str):
            geojson_content = json.loads(self.ROI)
        else:
            geojson_content = self.ROI

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
                return random_point

        raise RuntimeError("Unable to find a point inside any polygon.")
