import configparser
import os
from collections import defaultdict
from typing import Any, Dict


class ConfigReader:
    _config = None

    @classmethod
    def read_config(cls, file_name: str = "config.ini") -> Dict[str, Dict[str, Any]]:
        if cls._config is not None:
            return cls._config

        project_root = cls._find_project_root()
        config_file_path = os.path.join(project_root, file_name)

        config = configparser.ConfigParser()

        try:
            with open(config_file_path) as config_file:
                config.read_file(config_file)
        except FileNotFoundError:
            print(f"Error: The config file '{config_file_path}' was not found.")
            return {}
        except configparser.Error as e:
            print(
                f"Error: There was a problem"
                f" reading the config file '{config_file_path}': {e}"
            )
            return {}

        settings = defaultdict(dict)

        for section in config.sections():
            for key, value in config.items(section):
                settings[section][key] = cls._parse_value(value)

        cls._config = settings
        return settings

    @staticmethod
    def _parse_value(value: str) -> Any:
        if value.isdigit():
            return int(value)
        elif value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        elif "," in value:
            return [item.strip() for item in value.split(",")]
        else:
            return value

    @staticmethod
    def _find_project_root() -> str:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        while True:
            if os.path.exists(os.path.join(current_dir, "config.ini")):
                return current_dir
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                break
            current_dir = parent_dir
        raise Exception("Project root not found.")


# Example of usage - i keep it in comment
# if __name__ == "__main__":
#     # Find the root path of the project
#     project_root_path = find_root_path()
#
#     # Locate the config_v1.ini file in the project's root folder
#     config_file_path = os.path.join(project_root_path, "config_v1.ini")
#
#     # Read the config_v1.ini file
#     config_settings = read_config(config_file_path)
#
#     db_username = config_settings["DATABASE"]["username"]
#     db_password = config_settings["DATABASE"]["password"]
#     db_database = config_settings["DATABASE"]["database"]
#     db_port = config_settings["DATABASE"]["port"]
#
#     api_base_url = config_settings["API"]["base_url"]
#     api_timeout = config_settings["API"]["timeout"]
#     api_enable_logging = config_settings["API"]["enable_logging"]
#
#     enabled_features = config_settings["FEATURES"]["enabled_features"]
#
#     # Print the values
#     print(f"Database username: {db_username}")
#     print(f"Database password: {db_password}")
#     print(f"Database name: {db_database}")
#     print(f"Database port: {db_port}")
#     print(f"API base URL: {api_base_url}")
#     print(f"API timeout: {api_timeout}")
#     print(f"API enable logging: {api_enable_logging}")
#     print(f"Enabled features: {enabled_features}")
