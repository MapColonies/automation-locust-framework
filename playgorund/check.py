from common.config.config import config_obj
from common.utils.wfs_wrapper import WFSClient, GeoGenerator

geo_generator = GeoGenerator(ROI_PATH="/home/shayavr/Desktop/git/automation-locust-framework/test_data/roi.geojson")
bbox = geo_generator.get_random_bbox(min_width=config_obj["wfs"].MIN_WIDTH,
                                     max_width=config_obj["wfs"].MAX_WIDTH,
                                     min_height=config_obj["wfs"].MIN_HEIGHT,
                                     max_height=config_obj["wfs"].MAX_HEIGHT)

print(bbox)