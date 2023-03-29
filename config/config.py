import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Database:
    # ToDo: Fix the names.
    PG_USER = os.environ.get("pg_user", None)
    PG_PASS = os.environ.get("pg_pass", None)
    PG_PORT = os.environ.get("pg_port", None)
    PG_HOST = os.environ.get("pg_host", None)
    PG_JOB_TASK_DB_NAME = os.environ.get("pg_job_task_table", None)
    PG_RECORD_PYCSW_DB = os.environ.get("pg_pycsw_record_table", None)
    PG_MAPPROXY_CONFIG = os.environ.get("pg_mapproxy_table", None)
    PG_AGENT = os.environ.get("pg_agent_table", None)
    DISCRETE_AGENT_DB = os.environ.get("discrete_agent_db")
    HEARTBEAT_MANAGER = os.environ.get("heartbeat_manager")
    JOB_MANGER = os.environ.get("job_manager")
    LAYER_SPEC = os.environ.get("layer_spec")
    MAPPROXY_CONFIG = os.environ.get("mapproxy_config")
    RASTER_CATALOG = os.environ.get("raster_catalog_manager")
    PUBLIC = os.environ.get("public")


class Config:
    TOKEN = os.environ.get("SECRET_VALUE_API") or None
    HOST = os.environ.get("HOST", "enter a host")
    WAIT_TIME_FUNC = int(os.environ.get("wait_function", "4"))
    WAIT_TIME = int(os.environ.get("wait_time", "4"))
    MAX_WAIT = int(os.environ.get("max_wait", 1))
    MIN_WAIT = int(os.environ.get("min_wait", 1))
    LAYERS_LIST = (os.environ.get("layer_list", "test-update,shay")).split(",")


class WmtsConfig(Config):
    LAYER_TYPE = os.environ.get("layer_type", "wmts")
    LAYER_NAME = os.environ.get("layer", "OrthophotoHistory")
    GRID_NAME = os.environ.get("gridName", "default")
    IMAGE_FORMAT = os.environ.get("imageType", ".png")
    WMTS_CSV_PATH = os.environ.get("wmts_csv_path", "csv_data/data/new.csv")
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
