import json
import time

import requests
import random
from lxml import etree
from typing import List, Tuple
from shapely.geometry import shape, Polygon, MultiPolygon, Point
from locust import events



class WFSClient:
    """
    Wrapper for all WFS operations with Locust integration.
    """

    def __init__(self, base_url, version, token, output_format="application/json"):
        self.base_url = base_url
        self.version = version
        self.token = token
        self.output_format = output_format

    def _track_request(self, method, name, url, **kwargs):
        start_time = time.time()
        try:
            response = method(url, **kwargs)
            response.raise_for_status()
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(
                request_type=method.__name__.upper(),
                name=name,
                response_time=total_time,
                response_length=len(response.content),
            )
            return response
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type=method.__name__.upper(),
                name=name,
                response_time=total_time,
                exception=e,
            )
            raise

    def get_capabilities(self):
        params = {
            "service": "WFS",
            "request": "GetCapabilities",
            "version": self.version,
            "token": self.token
        }
        response = self._track_request(requests.get, "WFS GetCapabilities", self.base_url, params=params)
        return response.text

    def describe_feature_type(self, type_name):
        params = {
            "service": "WFS",
            "version": self.version,
            "request": "DescribeFeatureType",
            "typeNames": type_name,
            "token": self.token,
            "outputFormat": self.output_format
        }
        response = self._track_request(requests.get, "WFS DescribeFeatureType", self.base_url, params=params)
        return response.json() if self.output_format == "application/json" else response.text

    def get_feature(self, type_name, logic_operator=None, filters=None, request_params=None):
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

        if filters:
            headers = {"Content-Type": "application/xml"}
            filter_xml = self.create_wfs_filter(filters, logic_operator)
            response = self._track_request(
                requests.post,
                "WFS GetFeature (POST with Filter)",
                self.base_url,
                params=params,
                data=filter_xml,
                headers=headers
            )
        else:
            response = self._track_request(
                requests.get,
                "WFS GetFeature (GET)",
                self.base_url,
                params=params
            )

        return response.json() if self.output_format == "application/json" else response.text

    def transaction(self, transaction_xml):
        headers = {"Content-Type": "application/xml"}
        response = self._track_request(
            requests.post,
            "WFS Transaction",
            self.base_url,
            data=transaction_xml,
            headers=headers
        )
        return response.text

    @staticmethod
    def create_wfs_filter(
        filters: List[Tuple[str, str]],
        logic_operator: str = "And",
        ogc_version: str = "1.1.0"
    ) -> str:
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
