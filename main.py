import json
from hotels.HotelsRun import run_hotels
from Flights.travel_flights_pipeline import run_flights
import time

if __name__ == "__main__":
    user_text = (
        "Book me from dubai to Almaty for 2 adults from Jan 10/2026 to Jan 15/2026 cheapest and best options, "
        "in price range of 250 to 400 SAR per night, with free cancellation and pool and Free Wi-Fi."
    )

    
    start = time.perf_counter()
    TopFlights = run_flights(user_text)
    elapsed = time.perf_counter() - start

    print(f"run_flights took {elapsed:.3f} seconds\n\n")

    if TopFlights:
        print(json.dumps(TopFlights[0], indent=2, ensure_ascii=False))