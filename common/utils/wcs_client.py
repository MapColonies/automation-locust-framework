import math
import random
from xml.etree import ElementTree as ET
import requests
from requests.adapters import HTTPAdapter


class NoNormHTTPAdapter(HTTPAdapter):
    def request_url(self, request, proxies):
        return request.url # Return exactly what the user gave – no normalization

class WCSClient:

    def __init__ (self, base_url, version, token = None):
        self.base_url = base_url
        self.version = version
        self.token = token


    def get_coverage(self, coverage_id, format, subsets = None, additional_params= None, session = None):
        params = {
            "service": "WCS",
            "version": self.version,
            "request": "GetCoverage",
            "coverageId": coverage_id
        }

        if self.token:
            header = {"x-api-key": self.token}

        if subsets:
            params["subset"] = subsets

        if additional_params:
            params.update(additional_params)

        http_client = session if session else requests

        #set timeout?
        response = http_client.get(
            self.base_url, params=params, verify=False, headers=header)
        return response


    def extract_extent_from_xml(self, xml_string):
        """
        Parses a DescribeCoverage XML response and extracts the
        bounding box using possible GML namespace variations.

        Args:
            xml_string (str): The raw DescribeCoverage XML response

        Returns:
            tuple: (minx, miny, maxx, maxy)

        Raises:
            ValueError: If extent cannot be found in the XML
        """

        tree = ET.fromstring(xml_string)

        # Possible GML namespace variations
        gml_namespaces = [
            "{http://www.opengis.net/gml/3.2}",
            "{http://www.opengis.net/gml/3.1.1}",
            "{http://www.opengis.net/gml}",
        ]

        for gml in gml_namespaces:
            lower = tree.find(f".//{gml}lowerCorner")
            upper = tree.find(f".//{gml}upperCorner")

            if lower is not None and upper is not None:
                lower_vals = list(map(float, lower.text.split()))
                upper_vals = list(map(float, upper.text.split()))

                return (lower_vals[0], lower_vals[1], upper_vals[0], upper_vals[1])

        # Not found → raise useful error
        raise ValueError(
            "Could not find gml:lowerCorner and gml:upperCorner "
            "in DescribeCoverage response. Check XML structure or namespace."
        )

    def get_describe_coverage(self, coverage_id, session = None):
        """
        Sends a WCS DescribeCoverage request for a specific coverageId
        and returns its xml response.

        Args:
            coverage_id (str): The coverage/layer ID
            session (requests.Session, optional): An optional requests session to use

        Returns:
            xml

        Raises:
            RuntimeError: If the DescribeCoverage request fails
            RuntimeError: If XML parsing fails
        """

        params = {
            "version": "2.0.1",
            "request": "DescribeCoverage",
            "coverageId": coverage_id,
        }

        if self.token:
            headers = {
                "x-api-key": self.token
            }

        http_client = session if session else requests
        response = http_client.get(self.base_url, params=params, verify=False, headers=headers)

        if response.status_code != 200:
            raise RuntimeError(
                f"DescribeCoverage failed for {coverage_id}: "
                f"{response.status_code} {response.text}"
            )

        xml_string = response.text

        return xml_string

    def parse_coverage_metadata(self, xml_string):
        """
        Extracts:
          - extent (minx, miny, maxx, maxy)
          - axis labels (e.g. ["E","N"] or ["Long","Lat"])
          - CRS type (is_degree = True if EPSG:4326)

        Returns:
          (extent, axis_labels, is_degree)
        """
        tree = ET.fromstring(xml_string)

        # Find Envelope
        envelope = (
                tree.find(".//{http://www.opengis.net/gml/3.2}Envelope")
                or tree.find(".//{http://www.opengis.net/gml}Envelope")
        )
        if envelope is None:
            raise ValueError("Could not find gml:Envelope in XML")

        # Axis labels
        axis_labels_str = envelope.attrib.get("axisLabels")
        if not axis_labels_str:
            raise ValueError("Missing axisLabels in Envelope")

        axis_labels = axis_labels_str.split()

        # CRS (detect degrees)
        srs_name = envelope.attrib.get("srsName", "").lower()
        is_degree = "4326" in srs_name  # Only EPSG:4326 uses degrees

        # Extract extent
        lower = envelope.find("{http://www.opengis.net/gml/3.2}lowerCorner")

        upper = envelope.find("{http://www.opengis.net/gml/3.2}upperCorner")


        if lower is None or upper is None:
            raise ValueError("lowerCorner / upperCorner missing")

        minx, miny = map(float, lower.text.split())
        maxx, maxy = map(float, upper.text.split())

        extent = (minx, miny, maxx, maxy)

        return extent, axis_labels, is_degree

    def generate_subset(self, extent, width_m, height_m, axis_labels, is_degree):
        minx, miny, maxx, maxy = extent

        # Convert only if CRS is degree-based (EPSG:4326)
        if is_degree:
            center_lat = (miny + maxy) / 2.0
            center_lat_rad = math.radians(center_lat)

            width = width_m / (111320.0 * math.cos(center_lat_rad))
            height = height_m / 110540.0
        else:
            width = width_m  # CRS in meters → no conversion
            height = height_m

        # Validate
        if width > (maxx - minx):
            raise ValueError("Requested width exceeds coverage width")

        if height > (maxy - miny):
            raise ValueError("Requested height exceeds coverage height")

        # Random bbox inside extent
        rand_minx = random.uniform(minx, maxx - width)
        rand_miny = random.uniform(miny, maxy - height)

        rand_maxx = rand_minx + width
        rand_maxy = rand_miny + height

        axis_x, axis_y = axis_labels

        return [
            f"{axis_x}({rand_minx},{rand_maxx})",
            f"{axis_y}({rand_miny},{rand_maxy})"
        ]

    def generate_subset_from_xml(self, xml_string, width_m, height_m):
        """
        High-level helper:
          Input: XML + width_m + height_m
          Output: ready-to-use WCS subset[]
        """

        # Extract all metadata automatically
        extent, axis_labels, is_degree = self.parse_coverage_metadata(xml_string)

        # Generate subset correctly
        return self.generate_subset(extent, width_m, height_m, axis_labels, is_degree)

    def generate_subset_from_extent(self, extent, width_m, height_m):
        """
        extent = (minx, miny, maxx, maxy)
        width_m, height_m = requested bbox size IN METERS

        Converts meter sizes to degrees (EPSG:4326),
        validates, and returns WCS subset strings - such as:
            subsets = [
                "Long(10,20)",
                "Lat(30,40)"
            ]
        """

        minx, miny, maxx, maxy = extent

        # Compute center latitude for conversion accuracy
        center_lat = (miny + maxy) / 2.0
        center_lat_rad = math.radians(center_lat)

        # Convert meters → degrees
        width_deg = width_m / (111320.0 * math.cos(center_lat_rad))
        height_deg = height_m / 110540.0

        # Compute full width/height of coverage (in degrees)
        full_width_deg = maxx - minx
        full_height_deg = maxy - miny

        # Validate
        if width_deg > full_width_deg:
            raise ValueError(
                f"Requested width {width_m}m ({width_deg}°) exceeds coverage width "
                f"{full_width_deg}°. Maximum allowed width is {full_width_deg}°."
            )

        if height_deg > full_height_deg:
            raise ValueError(
                f"Requested height {height_m}m ({height_deg}°) exceeds coverage height "
                f"{full_height_deg}°. Maximum allowed height is {full_height_deg}°."
            )

        # Random left corner inside valid range
        rand_minx = random.uniform(minx, maxx - width_deg)
        rand_miny = random.uniform(miny, maxy - height_deg)

        rand_maxx = rand_minx + width_deg
        rand_maxy = rand_miny + height_deg

        return [
            f"Long({rand_minx},{rand_maxx})",
            f"Lat({rand_miny},{rand_maxy})"
        ]
