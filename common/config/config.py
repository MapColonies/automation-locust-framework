import json
import os


class Database:
    CONF_FILE = os.environ.get("CONF_FILE", "/home/shayavr/Downloads/new_locust_configuration.json")
    # CONF_FILE = os.environ.get("CONF_FILE", None)
    if not CONF_FILE:
        raise EnvironmentError("Should provide path for CONF_FILE")
    try:
        with open(CONF_FILE, "r", encoding="utf-8") as fp:
            conf = json.load(fp)
    except Exception as e:
        raise EnvironmentError("Failed to load JSON for configuration") from e
    print("-------------------------", conf)
    PG_CREDENTIAL =conf.get("pg_credential")
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
    HOST = os.environ.get("HOST", "enter a host")
    WAIT_TIME_FUNC = int(os.environ.get("wait_function", 4))
    WAIT_TIME = int(os.environ.get("wait_time", 4))
    MAX_WAIT = int(os.environ.get("max_wait", 1))
    MIN_WAIT = int(os.environ.get("min_wait", 1))
    LAYERS_LIST = os.environ.get("layer_list", "shay44").split(",")


class WmtsConfig(Config):
    LAYER_TYPE = os.environ.get("layer_type", "wmts")
    LAYER_NAME = os.environ.get("layer", "Orthophoto")
    GRID_NAME = os.environ.get("gridName", "newGrids")
    TOKEN = os.environ.get("SECRET_VALUE_API", None)
    # IMAGE_FORMAT = os.environ.get("imageType", ".png")
    IMAGE_FORMAT = os.environ.get("imageType", ".jpeg")
    WMTS_CSV_PATH = os.environ.get("wmts_csv_path", "test_data/wmts_shaziri.csv")
    REQUESTS_RECORDS_CSV = os.environ.get("requests_records_csv", f"{os.getcwd()}/tests/stats.csv")


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
    SHOH = (True,)
    LIRAN = False


class Config3D(Config):
    CSV_DATA_PATH = os.environ.get(
        "CSV_3D_DATA_PATH", "/home/shayavr/Desktop/git/automation-locust/urls_data.csv"
    )


config_obj = {
    "wmts": WmtsConfig,
    "pycsw": PycswConfig,
    "pro_active": ProActiveConfig,
    "_3d": Config3D,
    "default": Config,
}
