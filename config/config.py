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
    TOKEN = os.environ.get("SECRET_VALUE_API", ) or None
    HOST = os.environ.get("HOST", "enter a host")
    WAIT_TIME_FUNC = int(os.environ.get("wait_function", "4"))
    WAIT_TIME = int(os.environ.get("wait_time", "4"))
    MAX_WAIT = int(os.environ.get("max_wait", 1))
    MIN_WAIT = int(os.environ.get("min_wait", 1))
    LAYERS_LIST = (os.environ.get("layer_list", "test-update,shay")).split(",")
    RSP_TIME_RANGES = os.environ.get('rsp_time_ranges', [(0, 100), (101, 500), (501, None)])
    root_dir = os.environ.get('root_dir', '..') or None


class WmtsConfig(Config):
    LAYER_TYPE = os.environ.get("layer_type", "wmts")
    LAYER_NAME = os.environ.get("layer", "Orthophoto")  # History
    GRID_NAME = os.environ.get("gridName", "osm")
    IMAGE_FORMAT = os.environ.get("imageType", ".png")
    WMTS_CSV_PATH = os.environ.get("wmts_csv_path", "csv_data/data/new.csv")
    REQUESTS_RECORDS_CS = os.environ.get("requests_records_csv", f"{os.getcwd()}/tests/wmts_records.csv")
    WMTS_CSV_PATH_UPSCALE = os.environ.get("requests_records_upscale_csv", f"{os.getcwd()}/tests/upscale.csv")
    UP_SCALE_FLAG = os.environ.get("up_sacle_flag", False)
    WMTS_FLAG = os.environ.get("up_sacle_flag", False)


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
        "CSV_3D_DATA_PATH", " /home/shayperp/Desktop/Auto-projects/automation-locust-framework/urls_data.csv"
    )


class WmsConfig(Config):
    TOKEN = os.environ.get("TOKEN", True)
    TOK = os.environ.get("TOK",
                         'eyJhbGciOiJSUzI1NiIsImtpZCI6Ik1hcENvbG9uaWVzUUEifQ.eyJkIjpbInJhc3RlciIsInJhc3RlcldtcyIsInJhc3RlckV4cG9ydCIsImRlbSIsInZlY3RvciIsIjNkIl0sImlhdCI6MTY2Mzg2MzM0Mywic3ViIjoiTWFwQ29sb25pZXNRQSIsImlzcyI6Im1hcGNvbG9uaWVzLXRva2VuLWNsaSJ9.U_sx0Rsy96MA3xpIcWQHJ76xvK0PlHa--J1YILBYm2fCwtDdM4HLGagwq-OQQnBqi2e8KwktQ7sgt27hOJIPBHuONQS0ezBbuByk6UqN2S7P8WERdt8_lejuR1c94owQq7FOkhEaj_PKJ64ehXuMMHskfNeAIBf8GBN6QUGEenVx2w5k2rYBULoU30rpFkQVo8TtmiK2yGx0Ssx2k6LqSgCZfyZJbFzZ2MH3BPeCVleP1-zypaF9DS7SxS-EutL-gZ1e9bEccNktxQA4VMcjeTv45KYJLTIrccs_8gtPlzfaeNQFTIUKD-cRD1gyd_uLatPsl0wwHyFZIgRuJtcvfw')
    WIDTH = os.environ.get("WIDTH", 1800)
    HEIGHT = os.environ.get("HEIGHT", 900)
    LAYER_TYPE = os.environ.get("layer_type_wms", "dev-test-transparent-Orthophoto")
    GRID_NAME = os.environ.get("gridName", "default")
    IMAGE_FORMAT = os.environ.get("imageType", ".png")
    REQUESTS_RECORDS_CSV = os.environ.get("requests_records_csv", f"{os.getcwd()}/tests/stats.csv")
    HOST = os.environ.get("Host", 'https://mapproxy-raster-qa-route-raster-qa.apps.j1lk3njp.eastus.aroapp.io/')
    BBOX = os.environ.get("BBOX", [35.06068, 31.93225, 35.06270, 31.93316])
    WEB_MERCATOR_FLAG = os.environ.get("webMeractorFlag", False)
    WEB_MERCATOR = os.environ.get("webMeractor", None)
    REQUESTS_RECORDS_CS = os.environ.get("requests_records_csv", f"{os.getcwd()}/tests/stats.csv")
    SRS = os.environ.get("srs", "ESPG%3A4326")
    WMS_VERSION = os.environ.get("wms_version", "1.1.1")
    WMS_TRANSPARENT = os.environ.get("TRANSPARENT", True)
    STYLE = os.environ.get('STYLE', '')
    WMS_ZOOM_FLAG = os.environ.get("zoom_upscale_wms", False)
    # check git Capbility


config_obj = {
    "wms": WmsConfig,
    "wmts": WmtsConfig,
    "pycsw": PycswConfig,
    "pro_active": ProActiveConfig,
    "_3d": Config3D,
    "default": Config,
}
