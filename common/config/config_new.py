import json
import os


def get_env_variable(var_name, default=None, convert_type=None):
    try:
        val = os.environ.get(var_name, default)
        if convert_type is not None and val is not None:
            return convert_type(val)
        else:
            return val
    except Exception:
        print(f"Error getting environment variable: {var_name}")
        return None


def read_json_conf(file_path):
    try:
        with open(file_path, encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError:
        raise OSError(f"File {file_path} not found")
    except json.JSONDecodeError:
        raise OSError("Failed to decode JSON for configuration")


class Config:
    TOKEN = get_env_variable("SECRET_VALUE_API")
    HOST = get_env_variable("HOST", "enter a host")
    WAIT_TIME_FUNC = get_env_variable("wait_function", 4, int)
    WAIT_TIME = get_env_variable("wait_time", 4, int)
    MAX_WAIT = get_env_variable("max_wait", 1, int)
    MIN_WAIT = get_env_variable("min_wait", 1, int)
    LAYERS_LIST = get_env_variable("layer_list", "shay44").split(",")
    WMTS_CAPABILITIES_URL = get_env_variable("wmts_capabilities_url", "")
    RESULTS_PATH = get_env_variable("result_path", f"{os.getcwd()}")


class Database:
    CONF_FILE = get_env_variable(
        "CONF_FILE", "/home/shayavr/Downloads/new_locust_configuration.json"
    )
    conf = read_json_conf(CONF_FILE)
    PG_CREDENTIAL = conf.get("pg_credential", {})
    PG_SCHEMAS = conf.get("pg_schemas", {})
    PG_TABLES = conf.get("pg_tables", {})
    PG_USER = PG_CREDENTIAL.get("pg_user")
    PG_PASS = PG_CREDENTIAL.get("pg_pass")
    PG_PORT = PG_CREDENTIAL.get("pg_port")
    PG_HOST = PG_CREDENTIAL.get("pg_host")
    PG_RECORD_PYCSW_DB = PG_CREDENTIAL.get("pg_pycsw_record_table")
    PG_JOB_TASK_DB_NAME = get_env_variable("pg_job_task_table")
    PG_MAPPROXY_CONFIG = get_env_variable("pg_mapproxy_table")
    PG_AGENT = get_env_variable("pg_agent_table")
    DISCRETE_AGENT_DB = get_env_variable("discrete_agent_db")
    HEARTBEAT_MANAGER = get_env_variable("heartbeat_manager")
    JOB_MANAGER = get_env_variable("job_manager")
    LAYER_SPEC = get_env_variable("layer_spec")
    MAPPROXY_CONFIG = get_env_variable("mapproxy_config")
    RASTER_CATALOG = PG_SCHEMAS.get("raster_catalog_manager")
    PUBLIC = get_env_variable("public")


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
    elevation_host = os.environ.get("elevation_host_value", None)
    positions_path = os.environ.get(
        "positions_path_value",
        "/home/shayavr/Desktop/git/automation-locust-framework/test_data/myJson.json",
    )
    # headers = os.environ.get("headers_value", {'Content-Type': 'application/json', "Cache-Control": "no-cache"})
    headers = os.environ.get("headers_value", {"Content-Type": "application/json"})
    # headers = os.environ.get("headers_value", {'Content-Type': 'application/octet-stream', "Cache-Control": "no-cache"})
    results_path = os.environ.get("result_path", f"{os.getcwd()}")


class Config3D(Config):
    CSV_DATA_PATH = os.environ.get(
        "CSV_3D_DATA_PATH",
        "/home/shayavr/Desktop/git/automation-locust-framework/test_data/lol.csv",
    )


config_obj = {
    "wmts": WmtsConfig,
    "pycsw": PycswConfig,
    "pro_active": ProActiveConfig,
    "_3d": Config3D,
    "default": Config,
}
