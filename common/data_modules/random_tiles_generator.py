import xml.etree.ElementTree as ET
from typing import List

from mc_automation_tools import postgres

from common.config.config import ProActiveConfig, config_obj
from common.data_modules.get_all_layer import (
    create_mapproxy_layer_objects,
    create_zyx_tiles_structure,
)
from playgorund.config_backup import Database


def create_random_layer_tiles_urls(
    layer_name, tiles_list: List[tuple], image_format: str
):
    """
    This method return urls according to the z/y/x conventions from the list
    :param tiles_list: list of tile z/y/x
    :return: urls with the tile values
    """
    layer_tiles_urls = []

    for tile_value in tiles_list:
        url = (
            f"/{config_obj['wmts'].LAYER_TYPE}"
            f"/{layer_name}-{config_obj['wmts'].LAYER_NAME}"
            f"/{config_obj['wmts'].GRID_NAME}/{tile_value[0]}"
            f"/{tile_value[1]}/"
            f"{tile_value[2]}{image_format}"
            f"?token={config_obj['wmts'].TOKEN}"
        )
        layer_tiles_urls.append(url)
    return layer_tiles_urls


def query_random_layers_data() -> list:
    """
    this function will query the last x records and return the given columns values by selected name
    :param records_amount: records amount to be queries
    :param columns_name: the desired columns names to be queries
    :return:
    list of selected columns values on the selected records amount length
    """
    client = postgres.PGClass(
        host=Database.PG_HOST,
        database=Database.PG_RECORD_PYCSW_DB,
        user=Database.PG_USER,
        password=Database.PG_PASS,
        scheme=Database.RASTER_CATALOG,
        port=int(Database.PG_PORT),
    )
    res = client.get_records_by_limitation(
        column_names=ProActiveConfig.column_names,
        table_name="records",
        limitation_value=ProActiveConfig.layers_amount,
    )
    return res


def extract_values_from_nested_xml(xml_content: str, parent_name: str):
    # todo: edit the return object
    tree = ET.fromstring(xml_content)
    # Extract values from nested XML by parent name
    for parent_elem in tree.findall("parent"):
        if parent_elem.get("name") == parent_name:
            child_value = parent_elem.find("child").text
            return child_value


def get_image_format_from_capabilities(layers_data: list) -> dict:
    """
    This function returns the format of the image for each layer from  the selected layers
    :param layers_data: layer data from db query list ("product_id", max_resolution_deg", "product_bbox")
    :return:
    """
    pass


def create_random_layers_urls() -> list:
    """
    This method return a list of layers tiles urls for the proactive task
    :return:
    layers_url_list: list of all layers tiles
    """
    layers_urls = []
    random_layers_data = query_random_layers_data()
    mapproxy_objects_list = create_mapproxy_layer_objects(
        layers_data_list=random_layers_data
    )
    for layers_range in mapproxy_objects_list:
        z_y_x_structure = create_zyx_tiles_structure(
            zoom_value=layers_range["zoom_value"],
            y_range=layers_range["y_ranges"],
            x_range=layers_range["x_ranges"],
        )
        # todo: add function that return for each layer the image format!!
        layer_url = create_random_layer_tiles_urls(
            layers_range["layer_id"], z_y_x_structure, image_format=".png"
        )
        layers_urls.append(layer_url)
    return layers_urls
