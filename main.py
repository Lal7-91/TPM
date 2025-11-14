import json
from Flights.travel_flights_pipeline import run_flights
import time

if __name__ == "__main__":
    user_text = (
        "Book me from Dammam to Almaty for 2 adults from Jan 10/2026 to Jan 20/2026 cheapest and best options, "
        "in price range of 250 to 400 SAR per night, with free cancellation and pool and Free Wi-Fi."
    )

    
    start = time.perf_counter()
    TopFlights = run_flights(user_text)
    elapsed = time.perf_counter() - start

    print(f"run_flights took {elapsed:.3f} seconds\n\n")

    if TopFlights:
        print(json.dumps(TopFlights, indent=2, ensure_ascii=False))
    
    # time tolck to run
    time_taken = time.perf_counter() - start
    print(f"\nTotal time taken to run the flight booking pipeline: {time_taken:.2f} seconds")
    
# if __name__ == "__main__":
#     # Example user text — replace with real input when running
#     demo_user_text = "Return trip from DMM to ALA, depart 2026-01-10, return 2026-01-20, 2 adults, economy"
#     results = run_flights(demo_user_text)
#     print(f"\nFinal result count: {len(results)}")
#     # Print short summary for inspection
#     for i, rt in enumerate(results, start=1):
#         out = rt.get("outbound", {})
#         price = out.get("price")
#         flights = out.get("flights", [])
#         dep = flights[0]["departure_airport"]["id"] if flights and flights[0].get("departure_airport") else "N/A"
#         arr = flights[-1]["arrival_airport"]["id"] if flights and flights[-1].get("arrival_airport") else "N/A"
#         print(f"{i}. Outbound {dep}→{arr} price={price}, return options={len(rt.get('return_options', []))}")
