from config.config import config_obj, Config
from locust import between, task, FastHttpUser, tag

from test_data.queries import QUERY_TEMPLATE

polygon = {'name': config_obj["pycsw"].PYCSW_POLYGON_PROPERTY, 'value': config_obj["pycsw"].PYCSW_POLYGON_VALUE}
by_id = {'name': config_obj["pycsw"].PYCSW_ID_PROPERTY, 'value': config_obj["pycsw"].PYCSW_ID_VALUE}
by_region = {'name': config_obj["pycsw"].PYCSW_REGION_PROPERTY, 'value': config_obj["pycsw"].PYCSW_REGION_VALUE}




class SizingUser(FastHttpUser):
    between(1, 1)

    @tag("GetRecordsByPolygon")
    @task(1)
    def get_records_by_polygon(self):
        if config_obj["pycsw"].TOKEN_FLAG:
            self.client.post(
                f"?token={config_obj['pycsw'].Token}",
                data=QUERY_TEMPLATE(polygon).encode("UTF-8"),
                verify=False,
            )
        else:
            self.client.post(
                "/",
                data=QUERY_TEMPLATE(polygon).encode("utf-8"),
                verify=False,
            )

    @tag("GetRecordsByID")
    @task(1)
    def get_records_by_id(self):
        if config_obj["pycsw"].TOKEN_FLAG:
            self.client.post(
                f"?token={config_obj['pycsw'].Token}",
                data=QUERY_TEMPLATE(by_id).encode("utf-8"),
                verify=False,
            )
        else:
            self.client.post(
                "/",
                data=QUERY_TEMPLATE(by_id).encode("utf-8"),
                verify=False,
            )

    @tag("GetRecordsByRegion")
    @task(1)
    def get_records_by_region(self):
        if config_obj["pycsw"].TOKEN_FLAG:
            self.client.post(
                f"?token={config_obj['pycsw'].Token}",
                data=QUERY_TEMPLATE(by_region).encode("utf-8"),
                verify=False,
            )
            self.client.post(
                "/",
                data=QUERY_TEMPLATE(by_region).encode("utf-8"),
                verify=False,
            )

