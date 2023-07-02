import json
import os

from common.validation.validation_utils import extract_file_type

folder_path = "/home/shayavr/Desktop/test_data/update_new_fixed/check_something"


def read_tests_data_folder(folder_path: str):
    """
    this function will read the files that exist on the given folder path and return all file content as dictionary
    :param folder_path: path to the test data folder to be read
    :return:
    folder_files_content: dictionary of files names and contents
    """
    folder_files_content = {}
    for root, dirs, files in os.walk(folder_path):
        print(root)
        for file_name in files:
            print(file_name)
            file_type = extract_file_type(file_path=f"{root}/{file_name}")
            print(file_type)
            file_path = os.path.join(root, file_name)
            if file_type == "json":
                with open(file_path, "r") as file:
                    file_content = json.load(file)
                    # Process the file data as needed
                folder_files_content[f"{file_name}"] = file_content
            elif file_type == "bin":
                print("hey fron bin")
                with open(file_path, "rb") as file:
                    file_content = file.read()
                folder_files_content[f"{file_name}"] = f"{file_content}"
            else:
                with open(file_path, "r") as file:
                    file_content = file.read()
                    # Process the file data as needed
                folder_files_content[f"{file_name}"] = file_content
    return folder_files_content

print(read_tests_data_folder(folder_path=folder_path))