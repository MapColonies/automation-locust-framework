import os
import ijson
import csv

json_path = os.environ.get("INPUT_PATH")
output_csv_path = os.environ.get("OUTPUT_PATH")
filter_string = os.environ.get("STR_FILTER")


def extract_urls_from_f12_records(json_file_path, filter_string=None):
    urls = []
    with open(json_file_path, 'rb') as f:
        parser = ijson.items(f, 'log.entries.item')
        for entry in parser:
            if 'request' in entry and 'url' in entry['request']:
                url = entry['request']['url']
                if filter_string is None or filter_string in url:
                    urls.append(url)
    return urls


def write_urls_to_csv(urls, csv_file_path):
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URLs'])
        for url in urls:
            writer.writerow([url])


extracted_urls = extract_urls_from_f12_records(json_file_path=json_path, filter_string=filter_string)
write_urls_to_csv(extracted_urls, output_csv_path)
print(f"Filtered URLs containing '{filter_string}' have been written to '{output_csv_path}'.")
