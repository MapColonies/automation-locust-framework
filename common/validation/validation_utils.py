import bisect
import datetime
import json
import os
import re
from typing import Any, List, Union, Dict
import matplotlib.dates as mdates
import numpy as np
from matplotlib import pyplot as plt
import jsonschema


class ValidationError(Exception):
    pass


class KeyNotFoundError(ValidationError):
    pass


class ValueMismatchError(ValidationError):
    pass


class TypeMismatchError(ValidationError):
    pass


class LengthMismatchError(ValidationError):
    pass


def validate_response_status(response: Any, expected_status_code: int) -> None:
    if response.status_code != expected_status_code:
        raise ValueMismatchError(
            f"Expected status code {expected_status_code},"
            f" but got {response.status_code}"
        )


def validate_json_key_value(
        json_data: dict, key: str, expected_value: Union[str, int, float, bool]
) -> None:
    if key not in json_data:
        raise KeyNotFoundError(f"Key '{key}' not found in JSON data")
    if json_data[key] != expected_value:
        raise ValueMismatchError(
            f"Expected value for key '{key}' is {expected_value},"
            f" but got {json_data[key]}"
        )


def validate_json_keys(json_data: dict, expected_keys: List[str]) -> None:
    for key in expected_keys:
        if key not in json_data:
            raise KeyNotFoundError(f"Key '{key}' not found in JSON data")


def validate_json_array_length(json_array: List[Any], expected_length: int) -> None:
    if len(json_array) != expected_length:
        raise LengthMismatchError(
            f"Expected array length is {expected_length}, but got {len(json_array)}"
        )


def validate_json_key_type(json_data: dict, key: str, expected_type: type) -> None:
    if key not in json_data:
        raise KeyNotFoundError(f"Key '{key}' not found in JSON data")
    if not isinstance(json_data[key], expected_type):
        raise TypeMismatchError(
            f"Expected type for key '{key}' is {expected_type},"
            f" but got {type(json_data[key])}"
        )


def validate_json_array_contains(json_array: List[Any], expected_value: Any) -> None:
    if expected_value not in json_array:
        raise ValueMismatchError(
            f"Expected value '{expected_value}' not found in JSON array"
        )


def validate_json_key_regex(json_data: dict, key: str, regex_pattern: str) -> None:
    if key not in json_data:
        raise KeyNotFoundError(f"Key '{key}' not found in JSON data")
    if re.match(regex_pattern, json_data[key]) is None:
        raise ValueMismatchError(
            f"Value for key '{key}' does not match the regex pattern '{regex_pattern}'"
        )


def validate_json_key_not_present(json_data: dict, key: str) -> None:
    if key in json_data:
        raise KeyNotFoundError(f"Key '{key}' should not be present in JSON data")


def extract_file_type(file_path: str):
    """
    This function will extract from file path the file extension
    :param file_path: file location
    :return:
    file type value as str
    """
    if file_path and os.path.isfile(file_path):
        _, file_extension = os.path.splitext(file_path)
        return file_extension[1:] if file_extension else None
    else:
        return FileNotFoundError


def write_rps_percent_results(custom_path: str, percent_value_by_range: dict):
    """
    this function writes the percent result of the request per second ranges to JSON that located in the given path
    :param percent_value_by_range: dict of mill second range keys and the percent value of the request
    :param custom_path: a path that provided by user
    :return:
    """
    json_obj = json.dumps(percent_value_by_range)
    file_name = generate_unique_filename(file_base_name="percent_results")
    with open(f"{custom_path}/{file_name}", "w") as f:
        f.write(json_obj)


def generate_unique_filename(file_base_name: str):
    """
    this function generate unique name for runs results
    :return:
    """
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    formatted_time = now.strftime("%H-%M-%S")
    filename = f"{file_base_name}_{formatted_date}_{formatted_time}.json"
    return filename


def get_request_parameters(positions_list_path: str) -> [dict]:
    """
    this method will get the positions file path and return the body of the client request based on the type
    of the given position file path
    :param positions_list_path: position file path to be extract the request body type
    :return:
    dictionary of request parameters
    """
    request_type = extract_file_type(file_path=positions_list_path)
    if request_type == "json":
        with open(positions_list_path) as file:
            body = json.load(file)
            request_body = {
                "request_type": request_type,
                "body": body,
                "header": {"Content-Type": "application/json"},
            }
            return request_body
    elif request_type == "bin":
        with open(positions_list_path, "rb") as file:
            body = file.read()
            request_body = {
                "request_type": request_type,
                "body": body,
                "header": {"Content-Type": "application/octet-stream"},
            }
            return request_body
    else:
        return {
            "request_type": None,
            "body": "invalid position file path",
            "header": None,
        }


def read_tests_data_folder(folder_path: str):
    """
    this function will read the files that exist on the given folder path and return all file content as dictionary
    :param folder_path: path to the test data folder to be read
    :return:
    folder_files_content: dictionary of files names and contents
    """
    folder_files_content = {}
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_type = extract_file_type(file_path=f"{root}/{file_name}")
            file_path = os.path.join(root, file_name)
            if file_type == "json":
                with open(file_path) as file:
                    file_content = json.load(file)
                folder_files_content[f"{file_name}"] = file_content
            elif file_type == "bin":
                with open(file_path, "rb") as file:
                    file_content = file.read()
                folder_files_content[f"{file_name}"] = f"{file_content}"
            else:
                with open(file_path) as file:
                    file_content = file.read()
                folder_files_content[f"{file_name}"] = file_content
    return folder_files_content


def extract_points_from_json(json_file, excludeFields=True, product_type="MIXED"):
    """

    This function will be used as a ssn reader for json
    :param json_file: positions points file
    :param excludeFields : indicate if to send filed to be excluded
    :return:
    list of one point body
    """
    point_list = []
    with open(json_file) as file:
        data = json.load(file)
    if excludeFields:
        for point in data["positions"]:
            point_value = {
                "positions": [point],
                "productType": product_type,
                "excludeFields": [],
            }
            point_list.append(json.dumps(point_value))
    else:
        for point in data["positions"]:
            point_value = {
                "positions": [point],
                "productType": product_type,
                "excludeFields": ["productType", "updateDate", "resolutionMeter"],
            }
            point_list.append(json.dumps(point_value))
    return point_list


# def initiate_counters_by_ranges(config_ranges: List[tuple]) -> dict:
#     """
#     this function will extract the ranges and counter values for each value of range on the configuration
#     :param config_range_counter_data: selected configuration ranges data
#     :return:
#     counters (dict): counter for each given range
#     """
#     counters = {}
#     for i in range(len(config_ranges)):
#         counters[f"counter{i + 1}"] = 0
#     return counters


def initiate_counters_by_ranges(config_ranges: List) -> dict:
    """
    this function will extract the ranges and counter values for each value of range on the configuration
    :param config_ranges: selected configuration ranges
    :return:
    counter for each range (dict): counter for each given range
    """
    sorted_ranges = sorted(config_ranges)

    # Using list comprehension to create a tuple of lower and upper numbers
    lower_upper_tuples = [
        (sorted_ranges[i], sorted_ranges[i + 1]) for i in range(len(sorted_ranges) - 1)
    ]
    counters = {}
    for i in lower_upper_tuples:
        counters[f"{i}"] = 0
    return counters


def find_range_for_response_time(response_time, ranges_list, counters_dict):
    """
    This function will find response time value range for each given response time
    and will increase the range's counter
    :param response_time: response time of locust request
    :param ranges_list: list of ranges from configuration
    :param counters_dict: dictionary of each range value
    :return:
    updated counter_dict
    """
    index = bisect.bisect_left(ranges_list, response_time)

    # If the index is 0, the number is smaller than the first element in the list
    if index == 0:
        range_value = str((None, ranges_list[0]))
        counters_dict[range_value] += 1

    # If the index is equal to the list length, the number is greater than the last element in the list
    if index == len(ranges_list):
        range_value = str((ranges_list[-1], None))
        counters_dict[range_value] += 1

    # Otherwise, the number is located between two elements in the list
    lower_bound = ranges_list[index - 1]
    upper_bound = ranges_list[index]

    range_value = str((lower_bound, upper_bound))
    counters_dict[range_value] += 1

    return counters_dict


def create_custom_graph(graph_name, graph_path, test_results, graph_title=None):
    """
    This function will create graph from selected test results parameters
    :param graph_name: name of the output graph
    :param graph_path: path to store the graph file that created
    :param test_results: the selected parameters values for the graph presentation
    :param graph_title: graph name header
    :return: creating graph png file
    """
    parameters_names = list(test_results[0].keys())
    x_axis = parameters_names[0]
    y_axis = parameters_names[1]
    x_axis_data = [result[x_axis] for result in test_results]
    y_axis_data = [result[y_axis] for result in test_results]
    plt.plot(x_axis_data, y_axis_data, marker="o")
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    if not graph_title:
        plt.title(f"{x_axis} vs {y_axis}")
    else:
        plt.title(graph_title)
    plt.grid(True)
    plt.savefig(f"{graph_path}/{graph_name}.png")
    plt.close()


def create_graph_results_data_format(keys_names: list, x_y_axis_values: list) -> list:
    """
    This function will prepare the results data for graph creation funciton
    :param keys_names: the name of the data result (x axis data ,  y axis data )
    :param x_y_axis_values: list that contains two lists for each x-axis and y-axis results data
    :return:
    list of the results data by x axis and y axis keys
    """
    formatted_results = [
        {k: v for k, v in zip(keys_names, values)} for values in zip(*x_y_axis_values)
    ]
    return formatted_results


def create_start_time_response_time_graph(
        start_time_data, response_time_data, graph_name
):
    fig, ax = plt.subplots()
    x = np.array(start_time_data)  # X-coordinates of the data points
    y = np.array(response_time_data)  # Y-coordinates of the data points

    # Generate a unique color for each point
    num_points = len(x)
    colors = np.random.rand(num_points)

    plt.scatter(x, y, c=colors, cmap="viridis")
    ax.set_xlabel("Request Start Time")
    ax.set_ylabel("Response Time (ms)")
    ax.set_title("Request Start Time vs. Response Time")

    # Set the x-axis formatter
    formatter = mdates.DateFormatter("%H:%M:%S")
    formatter._useOffset = False  # Disable offset
    ax.xaxis.set_major_formatter(formatter)
    fig.autofmt_xdate()  # Auto-format the x-axis date labels
    scatter = plt.scatter(x, y, c=colors, cmap="viridis")
    plt.colorbar(scatter)
    plt.savefig(f"{graph_name}.png")
    plt.close()


def get_bulks_points_amount(bulk_content: dict):
    """
    This function will get bulk content and return the points amount by extracting
    the len of the positions
    :param bulk_content: the request's body of the bulk that contains points
    :return:
    points amount : int

    """
    points_amount = len(bulk_content["positions"])
    return points_amount


def retype_env(env_value: str):
    """
    This function will convert the value of the environment variable to the expected python type
    :param env_value: environment variable value - string type
    :return: the expected python type
    """
    if env_value.lower() == "none":
        return None

    if env_value.lower() == "true":
        return True
    if env_value.lower() == "false":
        return False

    try:
        return int(env_value)
    except ValueError:
        pass

    try:
        return float(env_value)
    except ValueError:
        pass

    if env_value.startswith("[") and env_value.endswith("]"):
        try:
            return list(map(retype_env, env_value[1:-1].split(",")))
        except ValueError:
            pass

    if env_value.startswith("{") and env_value.endswith("}"):
        try:
            items = [item.strip() for item in env_value[1:-1].split(",")]
            return {
                key.strip(): retype_env(val.strip())
                for key, val in [item.split(":") for item in items]
            }
        except (ValueError, IndexError):
            pass

    return env_value


# x = retype_env(env_value="[20,30,50,80,100,500]")
# print(retype_env(env_value="[20,30,50,80,100,500]"))
# x.append(0)
# x.append(float("inf"))
# percent_ranges = sorted(x)
# print(percent_ranges)


def find_keys_and_values_by_nested_value(value, input_dict, parent_key=None):
    key_value_pairs = []

    for key, val in input_dict.items():
        if isinstance(val, dict):
            nested_key_value_pairs = find_keys_and_values_by_nested_value(
                value, val, key
            )
            key_value_pairs.extend(nested_key_value_pairs)
        elif val == value:
            if parent_key:
                key_value_pairs.append((f"{parent_key}.{key}", val))
            else:
                key_value_pairs.append((key, val))

    return key_value_pairs


def parse_response_content(
        response_content: dict,
        response_time: float,
        normality_threshold: dict,
        property_name: str,
):
    """
    This function will parse elevation response by content values
    :param response_content: locust user response content
    :param  response_time: response time of users requests
    :param normality_threshold: response time dict with fast response time and slow response time
    :param property_name: the property name to be extracted from response content
    :return:
    if invalid return the request value
    """
    unusual_results = {}
    if (
            response_time <= normality_threshold["low_response_time"]
            or response_time >= normality_threshold["high_response_time"]
    ):
        unusual_results["anomaly_response_time"] = response_time
        unusual_results["response_body"] = [response_content]
    null_points = [
        item for item in response_content["data"] if item.get(property_name) is None
    ]
    if null_points:
        unusual_results["anomaly_response_time"] = response_time
        unusual_results["response_body"] = null_points

    return unusual_results


def sum_nested_dicts(nested_dict: dict):
    """
    This function will calculate the response time ranges counters of each worker
    for total response time percent by range
    :param nested_dict: dict with worker id as a keys and worker's counter as value
    :return:
    result: total requests count by each range for all workers
    """
    result = {}
    for key, data_dict in nested_dict.items():
        for nested_key, value in data_dict.items():
            if nested_key in result:
                result[nested_key] += value
            else:
                result[nested_key] = value

    return result


def find_unmatch_lat_long(request_points: dict, response_points: dict):
    """
    This function will return the unmatch points lat long value that returned from response content
    after validation
    :param request_points: request body points lat long values
    :param response_points: response points lat long values
    :return:
    list of unmatch lat long values
    """
    keys_to_compare = ['longitude', 'latitude']
    response_points = response_points["data"]
    request_points = request_points["positions"]
    validate_json_array_length(json_array=response_points, expected_length=len(request_points))
    request_points_set = set(json.dumps({k: x[k] for k in keys_to_compare}, sort_keys=True) for x in request_points)
    response_points_set = set(json.dumps({k: x[k] for k in keys_to_compare}, sort_keys=True) for x in response_points)
    return [json.loads(x) for x in response_points_set.difference(request_points_set)]


def find_unmatched_lat_long_points(request_dict: dict, response_dict: dict) -> List[Dict[str, float]]:
    """
    Return unmatched lat-long values from the response after validation.

    Args:
        request_dict (dict): Request body containing lat-long points.
        response_dict (dict): Response containing lat-long points.

    Returns:
        List[Dict[str, float]]: List of unmatched lat-long points.
    """
    request_positions = request_dict["positions"]
    response_data = response_dict["data"]

    validate_json_array_length(json_array=response_data, expected_length=len(request_positions))

    request_points_set = {(x['longitude'], x['latitude']) for x in request_positions}
    response_points_set = {(x['longitude'], x['latitude']) for x in response_data}

    unmatched_points = response_points_set.difference(request_points_set)
    return [{"longitude": lon, "latitude": lat} for lon, lat in unmatched_points]


def find_null_points(response_content: dict):
    """
    This function will return the points that returned height null value
    :param response_content:
    :return:
    list of lat long values of null heights
    """
    try:
        heights_list = response_content.get("data")
    except Exception as e:
        return e
    if len(heights_list) != 0:
        null_points = [
            item for item in heights_list if item.get("height") is None
        ]
        return null_points


def validate_response_body_schema(response_body: str, schema: dict):
    """
    This function will validate the response body schema
    :param response_body: response body string
    :param schema: python schema
    :return:
    dict of is valida flag and reason
    """
    is_response_valid = {"is_valid": True, "reason": ""}
    try:
        response_data = json.loads(response_body)
        jsonschema.validate(response_data, schema)
        return is_response_valid
    except json.JSONDecodeError:
        is_response_valid["is_valid"] = False
        is_response_valid["reason"] = "Error parsing response JSON."
        return is_response_valid
    except jsonschema.exceptions.ValidationError as e:
        is_response_valid["is_valid"] = False
        is_response_valid["reason"] = f"Response validation error: {e.message}"
        return is_response_valid

def find_unfounded_product_ids(response_data):
    """
    this function will find the product ids that wasn't found at the response products property
    :param response_data: requests response data (str)
    :return:
    list of unfounded product ids if exist
    """
    try:
        # Parse the JSON response
        response_data = json.loads(response_data)

        # Extract data and products
        data = response_data.get("data", [])
        products = response_data.get("products", {})

        # Get a list of all product IDs from the data property
        data_product_ids = [item.get("productId") for item in data]

        # Get the set of keys from the products property
        products_keys = set(products.keys())

        # Find unfound product IDs
        unfound_product_ids = [product_id for product_id in data_product_ids if product_id not in products_keys]

        return unfound_product_ids

    except json.JSONDecodeError:
        print("Error parsing JSON response.")
    except Exception as e:
        print(f"Validation error: {str(e)}")

    return []