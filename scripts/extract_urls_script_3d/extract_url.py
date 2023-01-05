import json
import os
import pandas as pd
from glom import glom


input_path = os.getenv("INPUT_PATH")
with open(input_path) as f:
    data_to_extract = json.load(f)
    f.close()

urls = glom(data_to_extract, ("log.entries", ["request.url"]))
urls_dict = {"url": urls}
df = pd.DataFrame(urls_dict)
df.to_csv(f"/csv_data/urls_data.csv")
