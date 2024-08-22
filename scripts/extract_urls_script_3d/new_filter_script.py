import csv
import os

import json
import os
import pandas as pd
from glom import glom
import common.config as cfg


input_path = "/home/shayavr/Downloads/raster_urls_records.json"
with open(input_path, "r") as f:
    data_to_extract = json.load(f)
    f.close()

urls = glom(data_to_extract, ("log.entries", ["request.url"]))
urls_dict = {"url": urls}
df = pd.DataFrame(urls_dict)
df.to_csv("/home/shayavr/Desktop/git/automation-locust-framework/test_data/unfiltered_urls.csv")



# Define the CSV file paths
# input_csv_file_path = os.environ.get('file_to_filter')
input_csv_file_path = "/home/shayavr/Desktop/git/automation-locust-framework/test_data/unfiltered_urls.csv"
# Replace with the path to your input CSV file
output_csv_file_path = f"/home/shayavr/Desktop/git/automation-locust-framework/test_data/filtered_urls.csv"  # Replace with the path for the output CSV file
# Define the specific string you want to search for
specific_string = "?token="
# List to store matching URLs
matching_urls = []


# Read the input CSV file and extract matching URLs
with open(input_csv_file_path, 'r', newline='') as input_csvfile:
    csvreader = csv.reader(input_csvfile)
    for row in csvreader:
        for url in row:
            if specific_string in url:
                matching_urls.append(url)
# Write the matching URLs to a new CSV file
with open(output_csv_file_path, 'w', newline='') as output_csvfile:
    csvwriter = csv.writer(output_csvfile)
    for url in matching_urls:
        csvwriter.writerow([url])
print(f"Matching URLs written to '{output_csv_file_path}'")