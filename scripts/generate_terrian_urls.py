import csv
import json
import itertools as it

path = "/home/shayavr/Desktop/git/automation-locust-framework/scripts/terrian_template.json"


def create_terrain_url_template(layer_metadata_path: str):
    """
    This function will create X,Y ,Z csv file for testing
    :param layer_metadata_path: layer metadata path for the x, y ,z ranges the url creation
    :return:
    True if the CSV file created
    """
    try:
        f = open("my_file.csv", "w")
        writer = csv.writer(f)
        with open(layer_metadata_path) as f:
            layer_metadata = json.load(f)
            print(layer_metadata)
        x_y_z_data = layer_metadata.get("available")

        for index, sublist in enumerate(x_y_z_data):
            # Check if sublist is empty
            if sublist:
                for item in sublist:
                    # Iterate through the range of X and Y values within the item's definition
                    for x in range(item["startX"], item["endX"] + 1):
                        for y in range(item["startY"], item["endY"] + 1):
                            writer.writerow([index, x, y])  # Print in desired format
        f.close()
    except Exception as e:
        print(f"Failed to extract test data, reason: {e}")
