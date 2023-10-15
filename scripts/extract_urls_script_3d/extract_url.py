import csv
import os
# Define the CSV file paths
input_csv_file_path = os.environ.get('file_to_filter')  # Replace with the path to your input CSV file
output_csv_file_path = f"{os.getcwd()}/filtered_urls.csv"  # Replace with the path for the output CSV file
# Define the specific string you want to search for
specific_string = os.environ.get("string_filter")
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