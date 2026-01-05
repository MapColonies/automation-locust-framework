import math
import random
from xml.etree import ElementTree as ET
import requests
from requests.adapters import HTTPAdapter
from typing import List, Tuple
from common.config.config import config_obj



class NoNormHTTPAdapter(HTTPAdapter):
    def request_url(self, request, proxies):
        return request.url # Return exactly what the user gave – no normalization

class WCSClient:

    def __init__ (self, base_url, version, token = None):
        self.base_url = base_url
        self.version = version
        self.token = token


    def get_coverage(self, coverage_id, format, subsets = None, session = None, additional_params= None):
        params = {
            "service": "WCS",
            "version": self.version,
            "request": "GetCoverage",
            "coverageId": coverage_id
        }

        # for key, value in kwargs.items():
        #     if value:
        #         params[key] = value

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

    def generate_subset_from_extent_by_size(self, extent, width_m, height_m, axis_labels, is_degree):
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


    def generate_subset_from_bbox(self, bbox_extent: str, axis_labels: Tuple[str, str]) -> List[str]:
        """
        Generates WCS SUBSET parameters directly mapping X to X and Y to Y.
        """
        try:
            cleaned_str = bbox_extent.strip("() '\"[]")
            coords = [float(s.strip()) for s in cleaned_str.split(',')]

            if len(coords) != 4:
                raise ValueError("BBOX string must contain exactly 4 comma-separated values.")

            # Standard GIS order: MinX (Long), MinY (Lat), MaxX (Long), MaxY (Lat)
            minx, miny, maxx, maxy = coords

        except ValueError as e:
            raise ValueError(f"Invalid BBOX string format: '{bbox_extent}'. Error: {e}")

        # Unpack axis labels. Assumed order from caller: (Axis X Label, Axis Y Label)
        # Example: axis_x='Long', axis_y='Lat'
        axis_x, axis_y = axis_labels

        # --- CORRECTION: Match X values to X axis, and Y values to Y axis ---

        # 1. X-Axis (Longitude / Easting) -> Takes MinX, MaxX
        subset_x = f"{axis_x}({minx},{maxx})"

        # 2. Y-Axis (Latitude / Northing) -> Takes MinY, MaxY
        subset_y = f"{axis_y}({miny},{maxy})"

        # Return list. The order inside the list usually doesn't matter for KVPs
        # as long as the strings themselves are correct.
        return [subset_y, subset_x]


    def generate_output_crs(self, output_crs, crs_dict):
        lookup_key = output_crs.lower()
        return crs_dict.get(lookup_key)

    def get_subset(self,extent, axis_labels, is_degree):
        if config_obj["wcs"].BBOX:
             return self.generate_subset_from_bbox(config_obj["wcs"].BBOX, axis_labels)
        return self.generate_subset_from_extent_by_size(extent, config_obj["wcs"].BBOX_WIDTH, config_obj["wcs"].BBOX_HEIGHT, axis_labels, is_degree)


    def generate_scalesize(self, pixel_sizes_str: str) -> str:
        """
        Generates the WCS SCALESIZE parameter string by parsing a string input
        from a configuration source and using the standard pixel axes ('i', 'j').

        The function enforces the use of 'i' for the X-axis (width) and 'j' for the
        Y-axis (height) as required by many WCS servers for SCALESIZE operations.

        Args:
            pixel_sizes_str (str): A string containing the desired pixel sizes,
                                   e.g., "'512,256'" or "(512, 256)".

        Returns:
            str: The full SCALESIZE string for the WCS request,
                 formatted as "i(SizeX),j(SizeY)".

        Raises:
            ValueError: If the input string format is incorrect or values are not integers.
        """

        # 1. Parsing the string input
        try:
            # Clean the string from outer quotes, parentheses, and any surrounding whitespace
            cleaned_str = pixel_sizes_str.strip("() '\"")

            # Split the string by the comma and strip any internal whitespace
            x_str, y_str = [s.strip() for s in cleaned_str.split(',')]

            # Convert the string parts to integers
            x_size = int(x_str)
            y_size = int(y_str)

        except ValueError as e:
            raise ValueError(
                f"Invalid pixel size format: '{pixel_sizes_str}'. Expected '(X,Y)' integers. Error details: {e}")

        # 2. Enforce the use of standard pixel axis labels ('i', 'j')
        # This ensures compliance with the WCS server's requirement for SCALESIZE.
        axis_x = 'i'
        axis_y = 'j'

        # 3. Format the SCALESIZE string components
        scale_size_x = f"{axis_x}({x_size})"
        scale_size_y = f"{axis_y}({y_size})"

        # 4. Combine and return the full parameter string
        return f"{scale_size_x},{scale_size_y}"