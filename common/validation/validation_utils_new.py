import datetime
import json
import os
import re
from http import HTTPStatus
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


def validate_response_status(response: Any, expected_status_code: HTTPStatus) -> None:
    """
    Validates the response status.
    """
    if response.status_code != expected_status_code:
        raise ValueMismatchError(
            f"Expected status code {expected_status_code.value},"
            f" but got {response.status_code}"
        )


def validate_json_key_value(
    json_data: dict, key: str, expected_value: Union[str, int, float, bool]
) -> None:
    """
    Validates the key-value pairs in the json.
    """
    if key not in json_data:
        raise KeyNotFoundError(f"Key '{key}' not found in JSON data")
    if json_data[key] != expected_value:
        raise ValueMismatchError(
            f"Expected value for key '{key}' is {expected_value},"
            f" but got {json_data[key]}"
        )


def validate_json_keys(json_data: dict, expected_keys: List[str]) -> None:
    """
    Validates the keys in the json.
    """
    for key in expected_keys:
        if key not in json_data:
            raise KeyNotFoundError(f"Key '{key}' not found in JSON data")


def validate_json_array_length(json_array: List[Any], expected_length: int) -> None:
    """
    Validates the length of the json array.
    """
    if len(json_array) != expected_length:
        raise LengthMismatchError(
            f"Expected array length is {expected_length}, but got {len(json_array)}"
        )


def validate_json_key_type(json_data: dict, key: str, expected_type: type) -> None:
    """
    Validates the type of the value for a particular key in the json.
    """
    if key not in json_data:
        raise KeyNotFoundError(f"Key '{key}' not found in JSON data")
    if not isinstance(json_data[key], expected_type):
        raise TypeMismatchError(
            f"Expected type for key '{key}' is {expected_type},"
            f" but got {type(json_data[key])}"
        )


def validate_json_array_contains(json_array: List[Any], expected_value: Any) -> None:
    """
    Validates if the json array contains the expected value.
    """
    if expected_value not in json_array:
        raise ValueMismatchError(
            f"Expected value '{expected_value}' not found in JSON array"
        )


def validate_json_key_regex(json_data: dict, key: str, regex_pattern: str) -> None:
    """
    Validates the regex pattern of the value for a particular key in the json.
    """
    if key not in json_data:
        raise KeyNotFoundError(f"Key '{key}' not found in JSON data")
    if re.match(regex_pattern, json_data[key]) is None:
        raise ValueMismatchError(
            f"Value for key '{key}' does not match the regex pattern '{regex_pattern}'"
        )


def validate_json_key_not_present(json_data: dict, key: str) -> None:
    """
    Validates if the key is not present in the json.
    """
    if key in json_data:
        raise KeyNotFoundError(f"Key '{key}' should not be present in JSON data")


def extract_file_type(file_path: str) -> str:
    """
    Extracts the file extension from the file path.
    """
    if file_path and os.path.isfile(file_path):
        _, file_extension = os.path.splitext(file_path)
        return file_extension[1:] if file_extension else None
    else:
        raise FileNotFoundError


def write_rps_percent_results(custom_path: str, percent_value_by_range: dict) -> None:
    """
    Writes the percent result of the request per second ranges to JSON located at the given path.
    """
    json_obj = json.dumps(percent_value_by_range)
    file_name = generate_unique_filename(file_base_name="percent_results")
    with open(os.path.join(custom_path, file_name), "w") as f:
        f.write(json_obj)


def generate_unique_filename(file_base_name: str) -> str:
    """
    Generates a unique name for the run results.
    """
    now = datetime.datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{file_base_name}_{formatted_date_time}.json"
    return filename
