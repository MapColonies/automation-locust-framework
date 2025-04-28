from locust import task, FastHttpUser, constant


class WfsUser(FastHttpUser):
    wait_time = constant(1)

    @task
    def get_feature(self):
        """
        Send a WFS GetFeature request using HTTP GET.
        """
        params = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "typename": "automation_2025_04_23_14_54_15-Orthophoto",  # <-- replace with your actual layer
            "outputFormat": "application/json",
            "srsName": "EPSG:4326",
            "bbox": "-180,-90,180,90"# Optional: request only a global bounding box
        }
        self.client.get("/wfs", params=params)
