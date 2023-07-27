import json
import os

import pandas as pd
from glom import glom

try:
    input_path = os.getenv("INPUT_PATH")
    with open(input_path) as f:
        data_to_extract = json.load(f)
except FileNotFoundError:
    print(
        "Error: File not found. Please check if the 'INPUT_PATH' environment variable is set correctly."
    )
    exit(1)
except json.JSONDecodeError:
    print("Error: Invalid JSON data in the input file.")
    exit(1)


urls = glom(data_to_extract, ("log.entries", ["request.url"]))
urls_dict = {"url": urls}

# cross-platform compatibility
output_path = os.path.join("test_data", "urls_data.csv")

# Improvement 4: Use a context manager (with statement) for file writing
try:
    df = pd.DataFrame(urls_dict)
    df.to_csv(output_path, index=False)
except Exception as e:
    print(f"Error occurred while writing to CSV: {e}")
    exit(1)

print(f"URL data successfully extracted and saved to '{output_path}'.")
