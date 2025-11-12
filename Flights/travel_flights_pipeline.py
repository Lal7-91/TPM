# travel_flights_pipeline.py

import os, json, ast, re
from dotenv import load_dotenv
from serpapi import GoogleSearch
from anthropic import Anthropic

# --------------------------------------------------------------------
# 1. SETUP
# --------------------------------------------------------------------
load_dotenv()

CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")
SERPAPI_KEY = os.environ.get("SERPAPI_KEY")

client = Anthropic(api_key=CLAUDE_API_KEY)


# --------------------------------------------------------------------
# 2. HELPER — GENERIC SAFE PARSER
# --------------------------------------------------------------------
def safe_parse(text):
    """Tries to safely parse stringified Python or JSON data."""
    if not isinstance(text, str):
        return text

    s = text.strip()
    if s.startswith("params"):
        s = s.split("=", 1)[1].strip()

    for parser in (ast.literal_eval, json.loads):
        try:
            return parser(s)
        except Exception:
            continue

    m = re.search(r'(\{.*\}|\[.*\])', s, re.DOTALL)
    if m:
        content = m.group(1)
        for parser in (ast.literal_eval, json.loads):
            try:
                return parser(content)
            except Exception:
                continue

    return None


# --------------------------------------------------------------------
# 3. LLM FUNCTION — GENERATE FLIGHT REQUEST PARAMETERS
# --------------------------------------------------------------------
def get_flight_request(user_input):
    try:
        with open("flights/prompts/flights_request_gen_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()
    except FileNotFoundError:
        print("flights_request_gen_prompt.txt not found")
        return None

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_input}]
    )

    raw = response.content[0].text.strip()
    return safe_parse(raw)


# --------------------------------------------------------------------
# 4. FETCH FLIGHTS FROM SERPAPI
# --------------------------------------------------------------------
def fetch_flights(params):
    params["api_key"] = SERPAPI_KEY
    search = GoogleSearch(params)
    allFlightsData = search.get_dict()

    os.makedirs("flights/JSONs", exist_ok=True)
    with open("flights/JSONs/flights.json", "w", encoding="utf-8") as f:
        json.dump(allFlightsData, f, indent=2)

    # Simplify to essential info for LLM
    clean_flights = []
    for flight_block in allFlightsData.get("best_flights", []) + allFlightsData.get("other_flights", []):
        clean_flights.append({
            "flights": [
                {
                    "airline": f.get("airline"),
                    "flight_number": f.get("flight_number"),
                    "airplane": f.get("airplane"),
                    "travel_class": f.get("travel_class"),
                    "departure_airport": f.get("departure_airport"),
                    "arrival_airport": f.get("arrival_airport"),
                    "duration": f.get("duration"),
                    "often_delayed_by_over_30_min": f.get("often_delayed_by_over_30_min")
                } for f in flight_block.get("flights", [])
            ],
            "layovers": [
                {
                    "name": l.get("name"),
                    "duration": l.get("duration")
                } for l in flight_block.get("layovers", [])
            ],
            "total_duration": flight_block.get("total_duration"),
            "carbon_emissions": flight_block.get("carbon_emissions", {}),
            "price": flight_block.get("price"),
            "type": flight_block.get("type")
        })

    with open("flights/JSONs/flights_filtered.json", "w", encoding="utf-8") as f:
        json.dump(clean_flights, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(clean_flights)} flights to flights_filtered.json")
    return clean_flights, allFlightsData


# --------------------------------------------------------------------
# 5. LLM FUNCTION — SELECT BEST FLIGHTS
# --------------------------------------------------------------------
def top_flights(flights, preferences, top_n=5):
    try:
        with open("flights/prompts/flights_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()
    except FileNotFoundError:
        print("flights_prompt.txt not found")
        return []

    user_input = (
        f"Here is the list of flights: {json.dumps(flights, ensure_ascii=False)}\n"
        f"User preferences: {preferences}\n"
        f"Please select the top {top_n} flights that best match these preferences "
        f"and return only a Python dictionary in the specified format."
    )

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_input}]
    )

    raw = response.content[0].text.strip()
    parsed = safe_parse(raw)

    if isinstance(parsed, dict) and "final_flights" in parsed:
        return parsed["final_flights"]
    elif isinstance(parsed, list):
        return parsed
    else:
        print("Failed to parse LLM output.")
        print(raw)
        return []


# --------------------------------------------------------------------
# 6. RUNNER FUNCTION
# --------------------------------------------------------------------
def run_flights(user_text: str):
    print("🔹 Generating flight search parameters...")
    params = get_flight_request(user_text)
    if not params:
        raise SystemExit("❌ Failed to generate flight parameters.")

    if isinstance(params, str):
        try:
            params = json.loads(params)
        except Exception:
            params = ast.literal_eval(params)

    os.makedirs("flights/JSONs", exist_ok=True)
    with open("flights/JSONs/flight_params.json", "w", encoding="utf-8") as f:
        json.dump(params, f, ensure_ascii=False, indent=2)

    print("✅ Flight parameters saved to flights/JSONs/flight_params.json")

    print("\n🔹 Fetching flight results from Google Flights...")
    flightsEssentialDetails, flightsFullData = fetch_flights(params)
    
    if not flightsEssentialDetails:
        raise SystemExit("❌ No flights found in API response.")

    print("\n🔹 Selecting best flights using LLM...")
    topFlights = top_flights(flightsEssentialDetails, user_text)
    if not topFlights:
        raise SystemExit("❌ Failed to get best flights from LLM.")

    print("\n✅ Successfully selected top flights.")
    return topFlights
