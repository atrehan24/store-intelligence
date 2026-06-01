import json
import requests

API_URL = "http://127.0.0.1:8000/events/ingest"

with open("data/sample_events.json", "r") as file:
    events = json.load(file)

response = requests.post(API_URL, json=events)

print("Status:", response.status_code)
print(response.json())