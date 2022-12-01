import itertools
import logging
import os

import pandas as pd

from common import Log as logger
from common.config import path_builder
from common.config import requests_file as CSV_NAME


def up_path(_path, n):
    return os.sep.join(_path.split(os.sep)[:-n])


# URL_TO_ITERATE = 'https://mapproxy.com/{TileMatrix}/{TileCol}/{TileRow}'
URL_TO_ITERATE = path_builder
logging = logger.MyLog()


def do_something():
    logging.info(f"Reading csv {CSV_NAME} file")
    csv_path = os.path.join(os.path.dirname(__file__), "data", CSV_NAME)

    try:
        df = pd.read_csv(csv_path)
        logging.info(f"csv read from {csv_path}")
    except FileNotFoundError as err:
        logging.error("Failed to read csv , file not found")
        raise FileNotFoundError(f"{CSV_NAME} in path : {csv_path}")

    x_column = df["TileMatrix"].tolist()
    y_column = df["TileCol"].tolist()
    z_column = df["TileRow"].tolist()

    logging.info("URL builder - looping on csv columns")

    url_list_to_run = []

    for (x, y, z) in zip(x_column, y_column, z_column):
        url_builder = URL_TO_ITERATE
        url_builder = url_builder.replace("TileMatrix", str(x))
        url_builder = url_builder.replace("TileCol", str(y))
        url_builder = url_builder.replace("TileRow", str(z))
        url_list_to_run.append(url_builder)
        # print(url_list_to_run)

    # print(df['x'].tolist())

    return url_list_to_run
