import csv
import json
import os
import random

metadata_file = os.environ.get('input')  # Replace with the path to your input CSV file
output_csv_file_path = os.environ.get('output')  # Replace with the path for the output CSV file
num_points_per_item = int(os.environ.get('tiles_number'))


def create_terrain_url_template(layer_metadata_path: str, output_csv_file_path: str, num_points_per_item: int):
    """
    This function will create X,Y ,Z csv file for testing
    :param layer_metadata_path: layer metadata path for the x, y ,z ranges the url creation
    :return:
    True if the CSV file created
    """
    try:
        f = open(output_csv_file_path, "w")
        writer = csv.writer(f)
        with open(layer_metadata_path) as f:
            layer_metadata = json.load(f)
            print(layer_metadata)
        x_y_z_data = layer_metadata.get("available")

        for index, sublist in enumerate(x_y_z_data):
            # Check if sublist is empty
            if sublist:
                for item in sublist:
                    # Generate random X and Y values within the range (inclusive)
                    for _ in range(num_points_per_item):
                        x = random.randint(item["startX"], item["endX"])
                        y = random.randint(item["startY"], item["endY"])
                        writer.writerow([index, x, y])

        f.close()
        print("Terrain script successfully completed!")
    except Exception as e:
        print(f"Failed to extract test data, reason: {e}")


if __name__ == "__main__":
    create_terrain_url_template(layer_metadata_path=metadata_file, output_csv_file_path=output_csv_file_path,
                                num_points_per_item=num_points_per_item)
