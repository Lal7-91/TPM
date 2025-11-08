import json
from hotels.HotelsRun import run_hotels
import time

if __name__ == "__main__":
    user_text = (
        "Book me a stay in Almaty for 2 adults from Jan 10/2026 to Jan 15/2026, "
        "in price range of 250 to 400 SAR per night, with free cancellation and pool and Free Wi-Fi."
    )

    
    start = time.perf_counter()
    TopHotels = run_hotels(user_text)
    elapsed = time.perf_counter() - start

    print(f"run_hotels took {elapsed:.3f} seconds\n\n")

    if TopHotels:
        print(json.dumps(TopHotels[0], indent=2, ensure_ascii=False))