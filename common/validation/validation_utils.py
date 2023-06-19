import datetime
import json
import os
import re
from typing import Any, List, Union


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


def write_rps_percent_results(custome_path: str, percente_value_by_range: dict):
    """
    this function writes the percent result of the request per second ranges to JSON that located in the given path
    :param custome_path: a path that provided by user
    :return:
    """
    json_obj = json.dumps(percente_value_by_range)
    file_name = generate_unique_filename(file_base_name="percent_results")
    with open(f"{custome_path}/{file_name}", "w") as f:
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
