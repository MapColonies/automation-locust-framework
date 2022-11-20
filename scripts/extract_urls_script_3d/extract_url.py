import json

import pandas as pd
from glom import glom

with open("/layerSources/shay_example.json", "r") as f:
    data_to_extract = json.load(f)
    f.close()

urls = glom(data_to_extract, ("log.entries", ["request.url"]))
urls_dict = {"url": urls}
df = pd.DataFrame(urls_dict)
df.to_csv("urls_data.csv")
