import configparser
import os


def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    # Read values from the configuration
    config.get("example_types", "description")
    config.get("example_types", "status")
    config.getboolean("example_types", "is_enabled")
    # Read the value as a string and split it into a list
    fruits_str = config.get("example_types", "fruits")
    [fruit.strip() for fruit in fruits_str.split(",")]
    # Read the value as a string
    api_key_str = config.get("example_types", "description")

    # Convert to None if the value is 'None', otherwise keep the original string
    None if api_key_str.lower() == "none" else api_key_str


if __name__ == "__main__":
    # Get the absolute path to the config.ini file in the root project folder
    parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file_path = os.path.join(parent_folder, "config.ini")

    config_data = read_config(config_file_path)
    print(config_data)
