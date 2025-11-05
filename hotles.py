from serpapi import GoogleSearch
import json
import os
from dotenv import load_dotenv

load_dotenv()

params = {
    "engine": "google_hotels",
    "q": "Riyadh hotels",
    "check_in_date": "2025-10-10",
    "check_out_date": "2025-10-11",
    "adults": "2",
    "sort_by": "8",
    "max_price": "500",
    "currency": "SAR",
    "gl": "us",
    "hl": "en",
    "api_key": os.environ.get("SERPAPI_KEY")
}

search = GoogleSearch(params)
results = search.get_dict()

with open("test.json", "w") as f:
    json.dump(results, f, indent=2)
