import json
import os


class Database:
    CONF_FILE = os.environ.get(
        "CONF_FILE", "/home/shayavr/Downloads/new_locust_configuration.json"
    )
    # CONF_FILE = os.environ.get("CONF_FILE", None)
    if not CONF_FILE:
        raise OSError("Should provide path for CONF_FILE")
    try:
        with open(CONF_FILE, encoding="utf-8") as fp:
            conf = json.load(fp)
    except Exception as e:
        raise OSError("Failed to load JSON for configuration") from e
    # print("-------------------------", conf)
    PG_CREDENTIAL = conf.get("pg_credential")
    PG_SCHEMAS = conf.get("pg_schemas")
    PG_TABLES = conf.get("pg_tables")
    PG_USER = PG_CREDENTIAL["pg_user"]
    PG_PASS = PG_CREDENTIAL["pg_pass"]
    PG_PORT = PG_CREDENTIAL["pg_port"]
    PG_HOST = PG_CREDENTIAL["pg_host"]
    PG_RECORD_PYCSW_DB = PG_CREDENTIAL["pg_pycsw_record_table"]
    # PG_RECORD_PYCSW_DB = PG_SCHEMAS["pg_pycsw_record_table"]
    PG_JOB_TASK_DB_NAME = os.environ.get("pg_job_task_table")
    PG_MAPPROXY_CONFIG = os.environ.get("pg_mapproxy_table")
    PG_AGENT = os.environ.get("pg_agent_table")
    DISCRETE_AGENT_DB = os.environ.get("discrete_agent_db")
    HEARTBEAT_MANAGER = os.environ.get("heartbeat_manager")
    JOB_MANAGER = os.environ.get("job_manager")
    LAYER_SPEC = os.environ.get("layer_spec")
    MAPPROXY_CONFIG = os.environ.get("mapproxy_config")
    RASTER_CATALOG = PG_SCHEMAS["raster_catalog_manager"]
    PUBLIC = os.environ.get("public")


class Config:
    TOKEN = os.environ.get("SECRET_VALUE_API", None)
    HOST = os.environ.get("HOST", "Enter a host")
    WAIT_TIME_FUNC = int(os.environ.get("wait_function", 4))
    WAIT_TIME = int(os.environ.get("wait_time", 4))
    MAX_WAIT = int(os.environ.get("max_wait", 1))
    MIN_WAIT = int(os.environ.get("min_wait", 1))
    LAYERS_LIST = os.environ.get("layer_list", "shay44").split(",")
    WMTS_CAPABILITIES_URL = os.environ.get("wmts_capabilities_url", "")
    RESULTS_PATH = os.environ.get("result_path", f"{os.getcwd()}")
    percent_ranges = os.environ.get("percent_ranges", [100, 500])


class WmtsConfig(Config):
    LAYER_TYPE = os.environ.get("layer_type", "wmts")
    LAYER_NAME = os.environ.get("layer", "Orthophoto")
    GRID_NAME = os.environ.get("gridName", "newGrids")
    TOKEN = os.environ.get("SECRET_VALUE_API", None)
    # IMAGE_FORMAT = os.environ.get("imageType", ".png")
    IMAGE_FORMAT = os.environ.get("imageType", ".jpeg")
    WMTS_CSV_PATH = os.environ.get("wmts_csv_path", "test_data/wmts_shaziri.csv")
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
    percent_ranges = os.environ.get("percent_ranges", [100, 500])
    bulks_root_folder = os.environ.get(
        "bulks_root_folder", "/home/shayavr/Documents/bulks_input"
    )
    wait_time = os.environ.get("wait_time", 1)
    graph_name = os.environ.get("graph_name", "avg_rps_vs_user_amount")
    payload_flag = os.environ.get("payload_flag", True)
    token_flag = os.environ.get("token_flag", True)
    # payload_flag = os.environ.get("payload_flag", True)
    # token_flag = os.environ.get("token_flag", True)
    points_amount_range = os.environ.get("points_amount_range", 5)
    poly = os.environ.get(
        "polygon",
        [
            [
                (35.21370173535735, 32.944784748967194),
                (35.21370173535735, 32.602044942336676),
                (35.76262909563465, 32.602044942336676),
                (35.76262909563465, 32.944784748967194),
                (35.21370173535735, 32.944784748967194),
            ],
            [
                (34.9936172458529, 32.73613049628601),
                (34.9936172458529, 32.431627293935804),
                (35.288205407997964, 32.431627293935804),
                (35.288205407997964, 32.73613049628601),
                (34.9936172458529, 32.73613049628601),
            ],
        ]
        # [
        #     [
        #         [
        #         ]
        #     ],
        #     [
        #         [
        #             [34.75686905280091, 30.674265565587575],
        #             [34.75686905280091, 30.668797385759987],
        #             [34.756895479083596, 30.668797385759987],
        #             [34.756895479083596, 30.674265565587575],
        #             [34.75686905280091, 30.674265565587575],
        #         ]
        #     ],
        # ],
    )
    exclude_fields = os.environ.get("exclude_fields", False)
    normality_threshold = os.environ.get(
        "normality_threshold", {"low_response_time": 20, "high_response_time": 800}
    )


class Config3D(Config):
    CSV_DATA_PATH = os.environ.get(
        "CSV_3D_DATA_PATH",
        "/home/shayavr/Desktop/git/automation-locust-framework/scripts/extract_urls_script_3d/filtered_urls.csv",
    )
    # PERCENT_RESULT_PATH = os.environ.get(
    #     # percent_result_path,
    # )


config_obj = {
    "wmts": WmtsConfig,
    "pycsw": PycswConfig,
    "pro_active": ProActiveConfig,
    "_3d": Config3D,
    "default": Config,
}
