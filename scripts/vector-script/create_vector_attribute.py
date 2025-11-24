import os
import requests
import json
from collections import defaultdict

# Config
type_name = os.getenv("TYPE_NAME", "buildings").strip()
base_url = os.getenv("URL", "https://geoserver-2-27-vector-dev.apps.j1lk3njp.eastus.aroapp.io/geoserver/core/wfs").rstrip('?&')
output_file = os.getenv("output_file", "attribute_value_mapping.json")

if not type_name:
    raise ValueError("Missing TYPE_NAME environment variable")


# Build full WFS GetFeature URL
full_url = (
    f"{base_url}"
    f"{'&' if '?' in base_url else '?'}"
    f"service=WFS&version=2.0.0&request=GetFeature"
    f"&typeNames={type_name}&outputFormat=application/json"
)

print("Fetching from:", full_url)

response = requests.get(full_url)
response.raise_for_status()
data = response.json()

# Process features as before
property_values = defaultdict(set)
for feature in data.get("features", []):
    for prop, val in feature.get("properties", {}).items():
        if val is not None:
            property_values[prop].add(val)

result = [
    {"attributeName": prop, "attributeValue": val, "typeNames": type_name}
    for prop, values in property_values.items()
    for val in values
]

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"Saved {len(result)} entries to {output_file}")
