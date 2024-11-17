import requests
import json
from requests.auth import HTTPBasicAuth

api_key = "IF5RWDZAE3SP6F4Z"
api_secret = "BMxAGetw/5x7FryuZPM+ENC4KVa+I80sz5xhbmDln2/76rN2IB557TpfirzB5XiT"
cluster_id = "lkc-66rpoq"

# Base URL for the Metrics API
base_url = "https://api.telemetry.confluent.cloud/v2/metrics/cloud"

# Endpoint for metric descriptors
endpoint = "/descriptors/metrics"

# Full URL
url = base_url + endpoint

# Send GET request
response = requests.get(url, auth=HTTPBasicAuth(api_key, api_secret))

# Check for successful response
if response.status_code == 200:
    data = response.json()
    # Print available metrics
    for metric in data["data"]:
        print(metric["name"])
else:
    print(f"Error: {response.status_code} - {response.text}")

query_payload = {
    "aggregations": [{"metric": "io.confluent.kafka.server/hot_partition_ingress"}],
    "granularity": "PT6H",  # 1-minute granularity
    "filter": {"field": "resource.kafka.id", "op": "EQ", "value": cluster_id},
    "limit": 1000,  # Adjust as needed
    "intervals": [
        "2024-11-16T00:00:00Z/2024-11-17T00:00:00Z"  # Replace with your desired time range
    ],
}
url = "https://api.telemetry.confluent.cloud/v2/metrics/cloud/query"
# Send POST request
response = requests.post(
    url,
    auth=HTTPBasicAuth(api_key, api_secret),
    headers={"Content-Type": "application/json"},
    data=json.dumps(query_payload),
)

# Check for successful response
if response.status_code == 200:
    data = response.json()
    # Process the data as needed
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.status_code} - {response.text}")
