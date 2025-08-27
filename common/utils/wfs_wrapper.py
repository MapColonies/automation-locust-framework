import json
import math

import requests
import random
from lxml import etree
from typing import List, Tuple, Union
from shapely.geometry import shape, Polygon, MultiPolygon, Point, box
from shapely.ops import unary_union
from common.utils.requests_logger import log_request


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

    def get_feature(
            self,
            logic_operator: str = None,
            filters: Union[str, List[Tuple[str, str]]] = None,
            feature_id: str = None,
            type_name: str = None,
            request_params: dict = None,
            method: str = "POST",
    ):
        """
        The GetFeature operation returns a selection of features from the data source.

        :param logic_operator: "And" or "Or" for combining filters (only if filters is a list).
        :param filters: Either a list of attribute filter tuples or a full XML string.
        :param feature_id: Optional feature ID to query a specific feature.
        :param type_name: Required if using feature_id.
        :param request_params: Additional query parameters.
        :param method: "GET" or "POST" (default is POST).
        """
        if feature_id and not type_name:
            raise ValueError("type_name must be provided when querying by feature_id")

        params = {
            "service": "WFS",
            "request": "GetFeature",
            "version": self.version,
            "outputFormat": self.output_format,
            "token": self.token
        }
        if request_params:
            params.update(request_params)

        headers = {}
        method = method.upper()

        # Build the XML body if needed
        data = ""
        if feature_id:
            data = f"""
            <wfs:GetFeature service="WFS" version="{self.version}"
                xmlns:wfs="http://www.opengis.net/wfs"
                xmlns:ogc="http://www.opengis.net/ogc">
                <wfs:Query typeName="{type_name}">
                    <ogc:Filter>
                        <ogc:FeatureId fid="{feature_id}"/>
                    </ogc:Filter>
                </wfs:Query>
            </wfs:GetFeature>
            """
            headers = {"Content-Type": "application/xml"}
        elif isinstance(filters, str):
            data = filters
            headers = {"Content-Type": "application/xml"}
        elif isinstance(filters, list):
            data = self.create_wfs_filter(filters, logic_operator)
            headers = {"Content-Type": "application/xml"}

        # Send request
        if method == "GET":
            response = self.session.get(self.base_url, params=params)
            log_request(method="GET", url=self.base_url, params=params, body=data, headers=headers)
        elif method == "POST":
            response = self.session.post(self.base_url, params=params, data=data, headers=headers)
            log_request(method="POST", url=self.base_url, params=params, body=data, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response

    def transaction(self, transaction_xml):
        headers = {"Content-Type": "application/xml"}
        response = self.session.post(self.base_url, data=transaction_xml, headers=headers)
        response.raise_for_status()
        return response

    @staticmethod
    def create_wfs_filter(
            filters: List[Tuple[str, str]] = None,
            feature_ids: List[str] = None,
            logic_operator: str = "And",
            ogc_version: str = "1.1.0"
    ) -> str:
        ogc_ns = {
            '1.1.0': 'http://www.opengis.net/ogc',
            '2.0': 'http://www.opengis.net/fes/2.0'
        }
        ns_uri = ogc_ns.get(ogc_version, ogc_ns['1.1.0'])
        ogc = etree.Element("{%s}Filter" % ns_uri)

        if feature_ids:
            for fid in feature_ids:
                etree.SubElement(ogc, "{%s}FeatureId" % ns_uri, fid=fid)

        elif filters:
            if len(filters) > 1:
                container = etree.SubElement(ogc, "{%s}%s" % (ns_uri, logic_operator))
            else:
                container = ogc
            for prop, value in filters:
                comp = etree.SubElement(container, "{%s}PropertyIsEqualTo" % ns_uri)
                prop_elem = etree.SubElement(comp, "{%s}PropertyName" % ns_uri)
                prop_elem.text = prop
                val_elem = etree.SubElement(comp, "{%s}Literal" % ns_uri)
                val_elem.text = value

        return etree.tostring(ogc, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode("utf-8")

    # @staticmethod
    # def create_wfs_filter(
    #         filters: List[Tuple[str, str]],
    #         logic_operator: str = "And",
    #         ogc_version: str = "1.1.0"
    # ) -> str:
    #     """
    #     Generates a WFS filter XML for a GetFeature request with multiple equality filters.
    #
    #     :param filters: List of (property_name, literal_value) tuples.
    #     :param logic_operator: Logical operator to combine filters: "And" or "Or".
    #     :param ogc_version: OGC version ("1.1.0" or "2.0").
    #     :return: XML string of the filter.
    #     """
    #     ogc_ns = {
    #         '1.1.0': 'http://www.opengis.net/ogc',
    #         '2.0': 'http://www.opengis.net/fes/2.0'
    #     }
    #
    #     ns_uri = ogc_ns.get(ogc_version, ogc_ns['1.1.0'])
    #
    #     ogc = etree.Element("{%s}Filter" % ns_uri)
    #
    #     if len(filters) == 1:
    #         container = ogc
    #     else:
    #         container = etree.SubElement(ogc, "{%s}%s" % (ns_uri, logic_operator))
    #
    #     for prop, value in filters:
    #         comp = etree.SubElement(container, "{%s}PropertyIsEqualTo" % ns_uri)
    #         prop_elem = etree.SubElement(comp, "{%s}PropertyName" % ns_uri)
    #         prop_elem.text = prop
    #         val_elem = etree.SubElement(comp, "{%s}Literal" % ns_uri)
    #         val_elem.text = value
    #
    #     return etree.tostring(ogc, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode("utf-8")

    @staticmethod
    def create_intersects_filter(pos_list: list[float], type_name: str) -> str:
        from lxml import etree

        NSMAP = {
            'wfs': "http://www.opengis.net/wfs/2.0",
            'fes': "http://www.opengis.net/fes/2.0",
            'gml': "http://www.opengis.net/gml/3.2",
            'xsi': "http://www.w3.org/2001/XMLSchema-instance",
            'my': "http://www.someserver.com/my"
        }

        # Ensure polygon is closed
        if pos_list[:2] != pos_list[-2:]:
            pos_list += pos_list[:2]

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

        query = etree.SubElement(root, "{http://www.opengis.net/wfs/2.0}Query", typeNames=type_name)
        filter_elem = etree.SubElement(query, "{http://www.opengis.net/fes/2.0}Filter")
        intersects = etree.SubElement(filter_elem, "{http://www.opengis.net/fes/2.0}Intersects")
        value_ref = etree.SubElement(intersects, "{http://www.opengis.net/fes/2.0}ValueReference")
        value_ref.text = "geom"

        polygon = etree.SubElement(intersects, "{http://www.opengis.net/gml/3.2}Polygon", srsName="EPSG:4326")
        exterior = etree.SubElement(polygon, "{http://www.opengis.net/gml/3.2}exterior")
        linear_ring = etree.SubElement(exterior, "{http://www.opengis.net/gml/3.2}LinearRing")
        pos_list_elem = etree.SubElement(linear_ring, "{http://www.opengis.net/gml/3.2}posList")
        pos_list_elem.text = " ".join(f"{x:.14f}" for x in pos_list)

        # Remove xml declaration to avoid GeoServer error
        return etree.tostring(root, pretty_print=True, xml_declaration=False, encoding='UTF-8').decode('utf-8')

    @staticmethod
    def create_wfs_point_dwithin_filter_body(
            point: str,
            distance: float,
            type_name: str = "buildings",
            srs_name: str = "EPSG:4326",
            property_name: str = "geom"
    ) -> str:
        """
        Creates a WFS 1.0.0 GetFeature request body using a DWithin spatial filter with a GML point.

        :param point: Coordinate string in format "x,y" (e.g., "593250,4923867")
        :param distance: Distance in meters
        :param type_name: Feature type name
        :param srs_name: Spatial reference system (e.g., "EPSG:4326")
        :param property_name: Geometry field name
        :return: XML string
        """
        NSMAP = {
            "wfs": "http://www.opengis.net/wfs",
            "ogc": "http://www.opengis.net/ogc",
            "gml": "http://www.opengis.net/gml",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }

        # Root element
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

        # Query
        query = etree.SubElement(root, "{http://www.opengis.net/wfs}Query", typeName=type_name)
        filter_elem = etree.SubElement(query, "{http://www.opengis.net/ogc}Filter")
        dwithin = etree.SubElement(filter_elem, "{http://www.opengis.net/ogc}DWithin")

        # PropertyName
        prop_elem = etree.SubElement(dwithin, "{http://www.opengis.net/ogc}PropertyName")
        prop_elem.text = property_name

        # GML Point
        gml_point = etree.SubElement(dwithin, "{http://www.opengis.net/gml}Point", srsName=srs_name)

        # Coordinates with proper formatting (no spaces around comma, strip whitespace)
        x, y = point.strip().split(",")
        coordinates = etree.SubElement(
            gml_point, "{http://www.opengis.net/gml}coordinates",
            decimal=".", cs=",", ts=" "
        )
        coordinates.text = f"{x.strip()},{y.strip()}"  # e.g., "593250,4923867"

        # Distance
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
        """
        if isinstance(self.ROI, str):
            with open(self.ROI, 'r') as file:
                geojson_content = json.load(file)
        else:
            raise ValueError(f"Invalid ROI path value - {self.ROI}")

        geometries = [shape(feature["geometry"]) for feature in geojson_content["features"]]
        merged_geom = unary_union(geometries)
        minx, miny, maxx, maxy = merged_geom.bounds

        # Clamp min/max sizes to ROI size
        roi_width = maxx - minx
        roi_height = maxy - miny
        min_width = min(min_width, roi_width)
        max_width = min(max_width, roi_width)
        min_height = min(min_height, roi_height)
        max_height = min(max_height, roi_height)

        for _ in range(200):  # allow more attempts
            bbox_width = random.uniform(min_width, max_width)
            bbox_height = random.uniform(min_height, max_height)

            x_range = roi_width - bbox_width
            y_range = roi_height - bbox_height
            if x_range <= 0 or y_range <= 0:
                continue

            rand_minx = random.uniform(minx, minx + x_range)
            rand_miny = random.uniform(miny, miny + y_range)
            candidate_bbox = box(rand_minx, rand_miny, rand_minx + bbox_width, rand_miny + bbox_height)

            # Check overlap area instead of just intersects
            if merged_geom.intersection(candidate_bbox).area > 0:
                return ", ".join(map(str, [rand_minx, rand_miny, rand_minx + bbox_width, rand_miny + bbox_height]))

        # fallback: return ROI bounding box
        return ", ".join(map(str, [minx, miny, maxx, maxy]))

    def generate_random_polygon(self, vertex_count: int, scale_factor: float = 0.01):
        """
        Generates a random polygon inside the ROI that intersects with actual features.

        Args:
            vertex_count (int): Minimum 4 (including closing vertex)
            scale_factor (float): fraction of ROI bounds for max radius

        Returns:
            list: [lon1, lat1, lon2, lat2, ..., lonN, latN] or None if failed
        """
        if vertex_count < 4:
            raise ValueError("vertex_count must be at least 4")

        # Load ROI GeoJSON
        if isinstance(self.ROI, str):
            with open(self.ROI, 'r') as f:
                geojson_obj = json.load(f)
        else:
            raise ValueError(f"Invalid ROI path value - {self.ROI}")

        # ROI geometry
        geom = shape(geojson_obj['features'][0]['geometry'])
        if isinstance(geom, MultiPolygon):
            geom = unary_union(geom)

        # Union of all features for intersection check
        features_union = unary_union([shape(f["geometry"]) for f in geojson_obj["features"]])

        minx, miny, maxx, maxy = geom.bounds

        for _ in range(1000):  # max attempts
            # Pick a random center point inside ROI
            cx, cy = None, None
            for _ in range(100):
                candidate = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
                if geom.contains(candidate):
                    cx, cy = candidate.x, candidate.y
                    break
            if cx is None:
                continue

            # Random radius in degrees, scaled by ROI size
            max_radius = min(maxx - minx, maxy - miny) * scale_factor
            radius = random.uniform(max_radius * 0.5, max_radius)

            # Generate polygon around center
            angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(vertex_count - 1)])
            coords = [(cx + radius * math.cos(a), cy + radius * math.sin(a)) for a in angles]
            coords.append(coords[0])  # close polygon

            candidate_poly = Polygon(coords)

            # Check polygon validity, containment, and intersection with data
            if candidate_poly.is_valid and geom.contains(candidate_poly):
                if candidate_poly.intersects(features_union):
                    # Flatten coordinates
                    return [round(c, 14) for pt in coords for c in pt]

        return None

# x = GeoGenerator(ROI_PATH="/home/shayavr/Desktop/git/automation-locust-framework/test_data/roi.geojson")
# print(x.generate_random_polygon(vertex_count=4))
