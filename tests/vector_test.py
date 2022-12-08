import os
import sys
import datetime
from pathlib import Path
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a = str(path.parent.absolute())
sys.path.append(a)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
from locust import SequentialTaskSet, HttpUser, constant, tag, task
import common.config as conf
import xmltodict
import random

numbers_of_req = os.getenv("req_amount") if os.getenv("req_amount") is not None else 25

class QueryService(SequentialTaskSet):

    # @task
    # @tag('start')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spatial_ope = None
        self.geo_oper = None
        self.get_feature_params = None

    def on_start(self):
        query_request = f"service=wfs&version=2.0.0&request=GetFeature&typeNames={conf.featureType}&outputFormat" \
                        f"=json&count={numbers_of_req}&sortBy=date "
        with self.client.get(query_request, catch_response=True, name="GetFeaturePostOnStart") as resp:
            print(resp.status_code)
            if 200 == resp.status_code:
                resp.success()
                get_params_req = resp.json()
                self.get_feature_params = get_params_req['features']
            else:
                resp.failure(str(resp.status_code) +" Query has sent "  +  query_request)

        query_request = f"service=wfs&version={conf.version}&request=GetCapabilities"
        with self.client.get(query_request, catch_response=True, name="GetCapabilitiesOnStart") as response:
            if 200 == response.status_code:
                response.success()
                get_params_req = xmltodict.parse(response.text)
                geo_ope = get_params_req['wfs:WFS_Capabilities']['fes:Filter_Capabilities']['fes:Spatial_Capabilities'][
                    'fes:SpatialOperators']['fes:SpatialOperator']
                spatial_ope = \
                    get_params_req['wfs:WFS_Capabilities']['fes:Filter_Capabilities']['fes:Spatial_Capabilities'][
                        'fes:GeometryOperands']['fes:GeometryOperand']
                self.geo_oper = [name['@name'] for name in geo_ope]
                self.spatial_ope = [name['@name'].replace("gml:", "") for name in spatial_ope]
            else:
                response.failure(str(response.status_code) +"Query has sent "  +  query_request)

    @task(1)
    @tag('GetCapabilities')
    def test_get_capabilities(self):
        query_request = f"service=wfs&version={conf.version}&request=GetCapabilities"
        with self.client.get(query_request, catch_response=True, name="GetCapabilities") as response:
            if 200 == response.status_code:
                response.success()
            else:
                response.failure(str(response.status_code) +"Query has sent "  +  query_request)

    @task(2)
    @tag('DescribeFeatureTypeGet')
    def test_describe_feature_type_get(self):
        query_request = f"service=wfs&version={conf.version}&request=DescribeFeatureType&typeNames={conf.featureType} "
        with self.client.get(query_request, catch_response=True, name="DescribeFeatureTypeGet") as response:
            if 200 == response.status_code:
                response.success()
            else:
                response.failure(str(response.status_code) +"Query has sent "  +  query_request)


    @task(1)
    @tag('GeometryFieldGet')
    def test_get_feature_geometry(self):
        bbox_cor_list = [random.uniform(conf.bbox_x[0], conf.bbox_x[-1]),
                         random.uniform(conf.bbox_x[0], conf.bbox_x[-1]),
                         random.uniform(conf.bbox_y[0], conf.bbox_y[-1]),
                         random.uniform(conf.bbox_y[0], conf.bbox_y[-1])]
        query_request = f"service=wfs&version={conf.version}&request=GetFeature&typeNames={conf.featureType}" \
                        f"&bbox={bbox_cor_list[0]},{bbox_cor_list[1]},{bbox_cor_list[2]},{bbox_cor_list[-1]}&" \
                        f"count={random.randrange(15)}"
        with self.client.get(query_request, catch_response=True, name="GeometryFieldGet/bbox") as response:
            if 200 == response.status_code:
                response.success()
            else:
                response.failure(str(response.status_code) +"Query has sent "  +  query_request)
    @task(1)
    @tag('GeometryFieldPost')  # must filters: by polygon, by MultiPolygon, by Envelope &count=6&type=Point
    def test_post_feature_geometry(self):
        query_request = f"service=wfs&version={conf.version}&request=GetFeature&typeNames={conf.featureType}&count={str(random.randint(1,9))}" \
                        f"&type={str(self.choice_params())}"
        with self.client.post(query_request, catch_response=True, name="GeometryFieldPost") as response:
            if 200 == response.status_code:
                print(response.text)
                response.success()
            else:
                response.failure(str(response.status_code) +" Query has sent "  +  query_request)


    @task(1)
    @tag('Date')
    def test_get_feature_date(self):
        start_date = datetime.datetime(2021, 1, 1)
        end_date = datetime.datetime.now()
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        ran_date = "'" + random_date.strftime("%x") + "'"
        query_request = f"service=wfs&version={conf.version}&request=GetFeature&typeNames={conf.featureType}&date={ran_date}"
        date_filter = random.choice(conf.by_date_filter)
        if "count" in date_filter:
            query_request+= date_filter + str(random.randint(1,9))
        else:
            query_request+= date_filter

        with self.client.post(query_request, catch_response=True, name="Date") as response:
            if 200 == response.status_code:
                #print(response.text)
                response.success()
            else:
                response.failure(str(response.status_code) +"Query has sent "  +  query_request)

    @task(1)
    @tag('GetFeatureGrid')
    def test_get_feature_grid(self):
        geo_id = self.choice_geo_pack()
        query_request = f"service=wfs&version={conf.version}&request=GetFeature&typeNames={conf.featureType}&featureId='{geo_id['id']}'"
        with self.client.post(query_request, catch_response=True, name="GetFeatureGfid") as response:
            if 200 == response.status_code:
                #print(response.text)

                response.success()
            else:
                response.failure(str(response.status_code) +"Query has sent "  +  query_request)

    def random_prams(self):
        random_geopackage = random.choice( self.spatial_ope)
        return random_geopackage

    def choice_geo_pack(self):
        chose = random.choice( self.get_feature_params)
        return chose

    def choice_params(self):
        return random.choice( self.geo_oper)


class MyLoadTest(HttpUser):
    tasks = [QueryService]
    wait_time = constant(1)
