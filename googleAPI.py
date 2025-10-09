from serpapi import GoogleSearch
import json
import os
from dotenv import load_dotenv

load_dotenv()

params = {
    "q": "Coffee",
    "location": "Austin, Texas, United States",
    "hl": "en",
    "gl": "us",
    "google_domain": "google.com",
    "api_key": os.environ.get("SERPAPI_KEY")
}

search = GoogleSearch(params)
results = search.get_dict()

with open("test.json", "w") as f:
    json.dump(results, f, indent=2)
