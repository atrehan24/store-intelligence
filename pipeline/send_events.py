import json
import requests

API_URL = "http://127.0.0.1:8000/events/ingest"

with open("data/generated_events.json", "r") as f:
    events = json.load(f)

response = requests.post(API_URL, json=events)

print("Status:", response.status_code)
print(response.json())