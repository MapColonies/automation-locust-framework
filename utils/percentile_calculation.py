import csv
import json
import os
import logging
import time

from config.config import Config, config_obj


def extract_response_time_from_record(csv_path: str):
    """
    This function return response time per request
    :param csv_path: path to the requests response time records
    :return:
    response_time_list: response time of requests
    """
    response_time_list = []
    if csv_path:
        with open(csv_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                response_time_list.append(float(row[2]))
    else:
        logging.info("Csv path not Found")

    return response_time_list


def get_percentile_value(rsp_avarage: list, rsp_total: int):
    """
    This function calculate the percentile value of the selected response time range of the total requests
    :param rsp_avarage: List of count results by definition of range
    :param rsp_total the total :
    :return:
    percentile_value: percent value : float
    """

    dict_results = {}
    for index, range in enumerate(Config.RSP_TIME_RANGES):
        dict_results[str(range)] = [rsp_avarage[index] / rsp_total * 100]
    return dict_results


def write_rsp_time_percentile_ranges(percentile_value: dict, file_name: str):
    json_obj = json.dumps(percentile_value)
    with open(f"{config_obj['wmts'].root_dir}/{file_name}-time_percentile_ran.json", 'w') as f:
        f.write(json_obj)


def calculate_times(csv_record_path, test_name):
    rsp_list = extract_response_time_from_record(csv_path=f"{config_obj['wmts'].root_dir}/{csv_record_path}")
    if len(rsp_list) == 0:
        logging.info(" List empty ")
        return None
    list_average = calculate_average(rsp_list)
    print(len(rsp_list))
    print(len(list_average))
    percentile_rages_dict = get_percentile_value(rsp_avarage=list_average, rsp_total=len(rsp_list))
    write_rsp_time_percentile_ranges(percentile_rages_dict, test_name)


def calculate_average(list_of_times: list):
    calculation = [0, 0, 0]
    for rsp in list_of_times:
        if rsp <= Config.RSP_TIME_RANGES[0][1]:
            calculation[0] += 1
        elif rsp <= Config.RSP_TIME_RANGES[1][1]:
            calculation[1] += 1
        else:
            calculation[2] += 1
    return calculation


def generate_name(name: str):
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    file_name = f"{name}-{current_time}-stats.csv'"
    return file_name


"""
Read me .
import the file to Your test class 
In configurion file add dir_root variable and give him path to the folder in your Environment 

For the  util to work at your Script test add the 2 lines in the start of the script after the imports out from the class  

file_name = generate_name(__name__)
stat_file = open(f"{config_obj['wmts'].root_dir}/{file_name}", 'w')

in the End of the Test class (Inside ) enter the next function

    def on_stop(self):
        calculate_times(file_name, __name__)
        
        
out of the class in the bottom add 2 listeners    

@events.request.add_listener
def hook_request_success(request_type, name, response_time, response_length, **kwargs):
    stat_file.write(f"{request_type};{name} ; {response_time};{response_length}  \n")


@events.quitting.add_listener
def hook_quitting(environment, **kw):
    stat_file.close()    

"""