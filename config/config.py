import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    TOKEN = os.environ.get("SECRET_VALUE_API") or None
    HOST = os.environ.get("HOST", "enter a host")
    WAIT_TIME_FUNC = (int(os.environ.get("wait_function", "4")),)
    WAIT_TIME = (int(os.environ.get("wait_time", "4")),)
    MAX_WAIT = (int(os.environ.get("max_wait", 1)),)
    MIN_WAIT = (int(os.environ.get("min_wait", 1)),)
    LAYERS_LIST = (os.environ.get("layer_list", "test-update,shay")).split(",")


class WmtsConfig(Config):
    LAYER_TYPE = os.environ.get("layer_type", "wmts")
    LAYER_NAME = os.environ.get("layer", "OrthophotoHistory")
    GRID_NAME = os.environ.get("gridName", "default")
    IMAGE_FORMAT = os.environ.get("imageType", ".png")
    WMTS_CSV_PATH = os.environ.get("wmts_csv_path", "csv_data/data/new.csv")


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
    CSV_DATA_PATH = "/home/shayavr/Desktop/git/automation-locust/urls_data.csv"


config_obj = {
    "wmts": WmtsConfig,
    "pycsw": PycswConfig,
    "pro_active": ProActiveConfig,
    "_3d": Config3D,
    "default": Config,
}
