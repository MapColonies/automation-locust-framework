import configparser
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict


class ConfigReader:
    def __init__(self, file_name: str = "config.ini"):
        self._config = None
        self.file_name = file_name

    def read_config(self) -> Dict[str, Dict[str, Any]]:
        if self._config is not None:
            return self._config

        project_root = self._find_project_root()
        config_file_path = project_root / self.file_name

        try:
            self._config = self._load_and_parse_config(config_file_path)
        except (FileNotFoundError, configparser.Error) as e:
            raise RuntimeError(f"Could not read config file: {e}")

        return self._config

    def _load_and_parse_config(self, file_path: Path) -> Dict[str, Dict[str, Any]]:
        config = configparser.ConfigParser()
        with open(file_path) as config_file:
            config.read_file(config_file)

        settings = defaultdict(dict)
        for section in config.sections():
            for key, value in config.items(section):
                settings[section][key] = self._parse_value(value)
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
    def _find_project_root() -> Path:
        current_dir = Path(__file__).parent
        while not (current_dir / ".git").exists():
            if current_dir.parent == current_dir:
                raise Exception("Project root not found.")
            current_dir = current_dir.parent
        return current_dir
