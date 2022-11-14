import os
from enum import Enum

basedir = os.path.abspath(os.path.dirname(__file__))


class Selection(Enum):
    WMTS = (1,)
    PYCSW = (2,)
    PRO_ACTIVE = (3,)
    CONFIG_3D = (4,)
    DEFAULT = 5


class Config:
    TOKEN = os.environ.get("SECRET_VALUE_API") or "hard to guess string"
    HOST = (os.environ.get("HOST") or "enter a host",)
    WAIT_TIME_FUNC = (int(os.environ.get("wait_function", "4")),)
    WAIT_TIME = (int(os.environ.get("wait_time", "4")),)


class WmtsConfig(Config):
    DOD = (True,)
    WMTS_CSV_PATH = "dsadasdas" or None


class PycswConfig(Config):
    TOT = True


class ProActiveConfig(Config):
    SHOH = (True,)
    LIRAN = False


class Config3D(Config):
    LOL = True


config = {
    Selection.WMTS: WmtsConfig,
    Selection.PYCSW: PycswConfig,
    Selection.PRO_ACTIVE: ProActiveConfig,
    Selection.CONFIG_3D: Config3D,
    Selection.DEFAULT: WmtsConfig,
}
