from locust import task, FastHttpUser, constant_pacing
from locust_plugins.csvreader import CSVReader
from common.config.config import config_obj, WmtsConfig

# Initialize the reader globally.
# It will automatically wrap around to the start of the file when it reaches the end.
wmts_csv_path = WmtsConfig.WMTS_CSV_PATH
ssn_reader = CSVReader(wmts_csv_path)

class WMTSUser(FastHttpUser):
    # Standard Locust wait time
    wait_time = constant_pacing(1)

    def on_start(self):
        """Pre-cache config values to avoid dictionary lookups during the test"""
        cfg = config_obj["wmts"]
        self.base_path = f"/{cfg.LAYER_TYPE}/{cfg.LAYER_NAME}/{cfg.GRID_NAME}/"
        self.img_format = cfg.IMAGE_FORMAT
        self.token = f"?token={cfg.TOKEN}" if cfg.TOKEN else ""

    @task
    def request_wmts_tile(self):
        # Use next() on the CSVReader instance
        # It returns a list or a dict depending on your CSV structure
        points = next(ssn_reader)
        z, x, y = points[0], points[1], points[2]

        # Build the URL
        # points[0]=Z, points[1]=X, points[2]=Y
        url = f"{self.base_path}{z}/{x}/{y}{self.img_format}{self.token}"

        # 'name' is CRITICAL for WMTS tests so the UI stays clean
        self.client.get(url, name=f"Zoom_Level_{z}")

    host = config_obj["wmts"].HOST