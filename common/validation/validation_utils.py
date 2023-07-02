import datetime
import json
import os
import re
from typing import Any, List, Union, Optional


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


def write_rps_percent_results(custom_path: str, percente_value_by_range: dict):
    """
    this function writes the percent result of the request per second ranges to JSON that located in the given path
    :param percente_value_by_range:
    :param custom_path: a path that provided by user
    :return:
    """
    json_obj = json.dumps(percente_value_by_range)
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
            request_body = {"request_type": request_type, "body": body,
                            "header": {"Content-Type": "application/json"}}
            return request_body
    elif request_type == "bin":
        with open(positions_list_path, "rb") as file:
            body = file.read()
            request_body = {"request_type": request_type, "body": body,
                            "header": {'Content-Type': 'application/octet-stream'}}
            return request_body
    else:
        return {"request_type": None, "body": "invalid position file path",
                "header": None}


def create_ranges_counters(ranges_list):
    ranges_counters = {}
    for range_val in ranges_list:
        ranges_counters[range_val] = 0
    return ranges_counters


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
                with open(file_path, "r") as file:
                    file_content = json.load(file)
                    # Process the file data as needed
                folder_files_content[f"{file_name}"] = file_content
            elif file_type == "bin":
                with open(file_path, "rb") as file:
                    file_content = file.read()
                folder_files_content[f"{file_name}"] = f"{file_content}"
            else:
                with open(file_path, "r") as file:
                    file_content = file.read()
                    # Process the file data as needed
                folder_files_content[f"{file_name}"] = file_content
    return folder_files_content

folder_path = "/home/shayavr/Desktop/test_data/update_new_fixed/check_something"

print(read_tests_data_folder(folder_path=folder_path))