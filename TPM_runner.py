# TPM_runner.py

import json, time
from concurrent.futures import ThreadPoolExecutor, as_completed

from Hotels.travel_hotels_pipeline import run_hotels
from Flights.travel_flights_pipeline import run_flights
from Activities.travel_things_pipeline import run_tripadvisor

def run_TPM(from_city, to_city, travelers, dates, stay_image, activities_percentages,
            run_hotels_flag=True, run_flights_flag=True, run_tripadvisor_flag=True,
            top_n_hotels=5, top_n_activities=5):
    
    start = time.perf_counter()

    # Construct user_text for hotels/flights
    user_text = f"Book a trip from {from_city} to {to_city} for {travelers} traveler(s) from {dates}"
    
    results = {}
    futures = {}

    with ThreadPoolExecutor(max_workers=3) as executor:
        if run_hotels_flag:
            futures[executor.submit(run_hotels, user_text)] = "hotels"
        if run_flights_flag:
            futures[executor.submit(run_flights, user_text)] = "flights"
        if run_tripadvisor_flag:
            futures[executor.submit(run_tripadvisor, to_city, activities_percentages)] = "tripadvisor"

        for future in as_completed(futures):
            key = futures[future]
            try:
                results[key] = future.result()
            except Exception as e:
                print(f"❌ Error in {key} pipeline: {e}")
                results[key] = None

    time_taken = time.perf_counter() - start
    print(f"\nTotal time taken to run TPM pipelines: {time_taken:.2f} seconds")
    return results


# -------------------------------
# Example Usage
# -------------------------------
if __name__ == "__main__":
    final_results = run_TPM(
        from_city="Dammam",
        to_city="Almmaty",
        travelers=1,
        dates="2026-01-10 to 2026-01-20",
        stay_image=None,
        activities_percentages={"nature": 60, "old/historical": 30, "modern": 10},
        run_hotels_flag=True,
        run_flights_flag=True,
        run_tripadvisor_flag=True
    )

    print(json.dumps(final_results, indent=2, ensure_ascii=False))
