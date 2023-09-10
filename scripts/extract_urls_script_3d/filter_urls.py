import csv
import os

import pandas as pd

# Define the CSV file path
csv_file_path = '/home/shayavr/Desktop/git/automation-locust-framework/test_data/urls_data_backup.csv'  # Replace with the path to your CSV file
output_csv_file_path = f"{os.getcwd()}/filtered_urls.csv"
# Define the specific string you want to search for
specific_string = '.b3dm?'

# List to store matching URLs
matching_urls = []

# Read the CSV file and extract matching URLs
with open(csv_file_path, 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        for url in row:
            if specific_string in url:
                matching_urls.append(url)

urls_dict = {"url": matching_urls}
df = pd.DataFrame(urls_dict)
df.to_csv(
    output_csv_file_path
)


# Write the matching URLs to a new CSV file
# with open(output_csv_file_path, 'w', newline='') as output_csvfile:
#     csvwriter = csv.writer(output_csvfile)
#     for url in matching_urls:
#         csvwriter.writerow([url])
#
# # # Print the matching URLs
# # for url in matching_urls:
# #     print(url)
# print(len(matching_urls))

import csv
import os
#
# # Define the CSV file paths
# input_csv_file_path = os.environ.get('file_to_filter')  # Replace with the path to your input CSV file
# output_csv_file_path = f"{os.getcwd()}/filtered_urls.csv"  # Replace with the path for the output CSV file
#
# # Define the specific string you want to search for
# specific_string = os.environ.get("string_filter")
#
# # List to store matching URLs
# matching_urls = []
#
# # Read the input CSV file and extract matching URLs
# with open(input_csv_file_path, 'r', newline='') as input_csvfile:
#     csvreader = csv.reader(input_csvfile)
#     for row in csvreader:
#         for url in row:
#             if specific_string in url:
#                 matching_urls.append(url)
#
# # Write the matching URLs to a new CSV file
# with open(output_csv_file_path, 'w', newline='') as output_csvfile:
#     csvwriter = csv.writer(output_csvfile)
#     for url in matching_urls:
#         csvwriter.writerow([url])
#
# print(f"Matching URLs written to '{output_csv_file_path}'")
