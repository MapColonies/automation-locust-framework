import json
import os
from plistlib import loads


class Config:
    TOKEN = os.environ.get("SECRET_VALUE_API", None)
    HOST = os.environ.get("HOST", "Enter a host")
    WAIT_TIME_FUNC = int(os.environ.get("wait_function", 1))
    WAIT_TIME = int(os.environ.get("wait_time", 1))
    MAX_WAIT = int(os.environ.get("max_wait", 1))
    MIN_WAIT = int(os.environ.get("min_wait", 1))
    LAYERS_LIST = os.environ.get("layer_list", "shay44").split(",")
    WMTS_CAPABILITIES_URL = os.environ.get("wmts_capabilities_url", "")
    RESULTS_PATH = os.environ.get("result_path", f"{os.getcwd()}")
    percent_ranges = os.environ.get("percent_ranges", [100, 500])
    MAX_ROWS_PER_FILE = os.environ.get("MAX_ROWS_PER_FILE", 5000)
    OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "request_logs")


class WmtsConfig(Config):
    LAYER_TYPE = os.environ.get("layer_type", "wmts")
    LAYER_NAME = os.environ.get("layer", "aza_south-Orthophoto")
    GRID_NAME = os.environ.get("gridName", "WorldCRS84")
    TOKEN = os.environ.get("SECRET_VALUE_API", None)
    IMAGE_FORMAT = os.environ.get("imageType", ".png")
    # IMAGE_FORMAT = os.environ.get("imageType", ".jpeg")
    WMTS_CSV_PATH = os.environ.get("wmts_csv_path", "test_data/tiles.csv")
    REQUESTS_RECORDS_CSV = os.environ.get(
        "requests_records_csv", f"{os.getcwd()}/tests/stats.csv"
    )


class PycswConfig(Config):
    PYCSW_ID_PROPERTY = os.environ.get("mc_id_property", "mc:id")
    PYCSW_REGION_PROPERTY = os.environ.get("mc_region_property", "mc:region")
    PYCSW_POLYGON_PROPERTY = os.environ.get(
        "mc_polygon_property", "mc:layerPolygonParts"
    )
    PYCSW_ID_VALUE = os.environ.get(
        "mc_id_value", "d53a03e3-650b-4f4e-9047-071667741c08"
    )
    PYCSW_REGION_VALUE = os.environ.get("mc_region_value", "string")
    PYCSW_POLYGON_VALUE = os.environ.get("mc_polygon_value", "s")


class ProActiveConfig(Config):
    pyscw_host = os.environ.get("pyscw_host_value", None)
    wmts_host = os.environ.get("wmts_host_value", None)
    layers_amount = os.environ.get("layers_amount", None)
    column_names = ["product_id", "max_resolution_deg", "product_bbox"]
    db_for_query = "records"


class ElevationConfig(Config):
    response_schema = {
        "type": "object",
        "required": ["data", "products"],
        "properties": {
            "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["longitude", "latitude", "height"],
                    "properties": {
                        "longitude": {
                            "type": "number",
                            "format": "double"
                        },
                        "latitude": {
                            "type": "number",
                            "format": "double"
                        },
                        "height": {
                            "type": "number",
                            "nullable": True,
                            "format": "double"
                        },
                        "productId": {
                            "type": "string"
                        }
                    }
                }
            },
            "products": {
                "type": "object",
                "additionalProperties": {
                    "type": "object",
                    "properties": {
                        "productType": {
                            "oneOf": [
                                {"$ref": "#/definitions/productTypeEnum"}
                            ]
                        },
                        "resolutionMeter": {
                            "type": "number",
                            "format": "double"
                        },
                        "absoluteAccuracyLEP90": {
                            "type": "number",
                            "format": "double"
                        },
                        "updateDate": {
                            "type": "string",
                            "format": "date-time"
                        }
                    }
                }
            }
        },
        "definitions": {
            "productTypeEnum": {
                "type": "string",
                "enum": ["DSM", "DTM", "MIXED"]
            }
        }
    }
    elevation_host = os.environ.get("elevation_host_value", None)
    positions_path = os.environ.get(
        "positions_path_value",
        "/home/shayavr/Desktop/git/automation-locust-framework/test_data/myJson.json",
    )
    headers = os.environ.get(
        "headers_value",
        {"Content-Type": "application/octet-stream", "Cache-Control": "no-cache"},
    )
    results_path = os.environ.get("results_path", f"{os.getcwd()}")
    # percent_ranges = os.environ.get(
    #     "percent_ranges", [(0, 100), (101, 500), (501, float('inf'))]
    # )
    percent_ranges = os.environ.get(
        "percent_ranges", [100, 500]
    )

    bulks_root_folder = os.environ.get(
        "bulks_root_folder", "/home/shayavr/Documents/bulks_input"
    )
    wait_time = os.environ.get("wait_time", 1)
    graph_name = os.environ.get("graph_name", "avg_rps_vs_user_amount")
    terrain_csv_path = os.environ.get("terrain_csv_path",
                                      "/home/shayavr/Desktop/git/automation-locust-framework/test_data/new.csv")
    payload_flag = os.environ.get("payload_flag", True)
    token_flag = os.environ.get("token_flag", True)
    # payload_flag = os.environ.get("payload_flag", True)
    # token_flag = os.environ.get("token_flag", True)
    points_amount_range = os.environ.get("points_amount_range", 5)
    poly = os.environ.get(
        "polygon",
        [[
            (34.78599261466954, 30.62650484692135),
            (34.78599261466954, 30.56735846770877),
            (34.873818350199315, 30.56735846770877),
            (34.873818350199315, 30.62650484692135),
            (34.78599261466954, 30.62650484692135),
        ],
            [
                (34.75686905280091, 30.674265565587575),
                (34.75686905280091, 30.668797385759987),
                (34.756895479083596, 30.668797385759987),
                (34.756895479083596, 30.674265565587575),
                (34.75686905280091, 30.674265565587575),
            ]
        ]
    )
    exclude_fields = os.environ.get("exclude_fields", True)
    TERRAIN_lAYER = os.environ.get("layer_type", "terrains")
    TERRAIN_NAME = os.environ.get("terrain_name", "combined_srtm_30_100_il_ever")
    TERRAIN_FORMAT = os.environ.get("terrain_format", ".terrain")


class Config3D(Config):
    CSV_DATA_PATH = os.environ.get(
        "CSV_3D_DATA_PATH",
        "/home/shayavr/Desktop/git/automation-locust-framework/test_data/lol.csv",
    )
    exclude_fields = os.environ.get("exclude_fields", False)
    normality_threshold = os.environ.get(
        "normality_threshold", {"low_response_time": 20, "high_response_time": 800}
    )


class WfsConfig(Config):
    REQUEST_METHOD = os.getenv("REQUEST_METHOD", "POST")
    BBOX_MAPPING = os.getenv("BBOX_MAPPING",
                             "/home/shayavr/Desktop/git/automation-locust-framework/test_data/type_by_bbox.json")
    ATTRIBUTE_MAPPING = os.getenv("ATTTRIBUTE_MAPPING",
                                  "/home/shayavr/Desktop/git/automation-locust-framework/test_data/attribute_query.json")
    WFS_URL = os.getenv("WFS_URL",
                        "https://geoserver-2-27-vector-dev.apps.j1lk3njp.eastus.aroapp.io/geoserver/core/wfs")
    MIN_RADIUS = int(os.getenv("MIN_RADIUS", 100))
    MAX_RADIUS = int(os.getenv("MAX_RADIUS", 5000))
    VERSION = os.getenv("VERSION", "2.0.0")
    ID_LIST = os.getenv("ID_LIST",
                        ["004CAF38-2758-99B6-6A29-6E648A5CA573", "03C9B549-AA0C-8164-84FF-819755085F6B4"])
    ROI_PATH = os.environ.get("ROI_PATH", "/home/shayavr/Desktop/git/automation-locust-framework/test_data/roi.geojson")
    TYPE_NAMES = os.environ.get("TYPE_NAMES", '{"key":"SWAP_TEST-RasterVectorBest"}')
    MIN_WIDTH = float(os.environ.get("MIN_WIDTH", 1))
    MAX_WIDTH = float(os.environ.get("MAX_WIDTH", 100))
    MIN_HEIGHT = float(os.environ.get("MIN_HEIGHT", 1))
    MAX_HEIGHT = float(os.environ.get("MAX_HEIGHT", 100))
    VERTEX_COUNT = int(os.environ.get("VERTEX_COUNT", 5))
    SRS_NAME = os.environ.get("SRS_NAME", "EPSG:4326")
    PROPERTY_NAME = os.environ.get("PROPERTY_NAME", "geom")
    TYPE_NAME = os.environ.get("TYPE_NAME", "buildings")

class WcsConfig(Config):
    BASE_URL = os.environ.get("WCS_URL", "https://dem-geoserver-pp-geoserver-nginx-route-qa.apps.j1lk3njp.eastus.aroapp.io//wcs")
    VERSION = os.environ.get("WCS_VERSION", "2.0.1")
    # COVERAGE_ID = os.environ.get("COVERAGE_ID", "dtm_srtm30wgs84utm36_COG")
    COVERAGE_ID = os.environ.get("COVERAGE_ID", "dtm_srtm30wgs84geo_untiled")
    BBOX_WIDTH = int(os.environ.get("BBOX_WIDTH", 50)) #in meters
    BBOX_HEIGHT = int(os.environ.get("BBOX_HEIGHT", 50)) #in meters
    RESOLUTIONS = { "resx": os.environ.get("RES_X", 5), "resy": os.environ.get("RES_Y", 5)}
    SCALE_SIZE = os.environ.get("SCALE_SIZE","256,256")  # Exactly 256×256 pixels output
    FORMAT = os.environ.get("WCS_FORMAT", "image/tiff")




config_obj = {
    "wmts": WmtsConfig,
    "pycsw": PycswConfig,
    "pro_active": ProActiveConfig,
    "_3d": Config3D,
    "default": Config,
    "elevation": ElevationConfig,
    "wfs": WfsConfig,
    "wcs": WcsConfig,

}
