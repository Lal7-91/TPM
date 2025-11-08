import streamlit as st
import datetime
import json
from hotels.HotelsRun import run_hotels
import time

st.set_page_config(page_title="Travel Planner", page_icon="🧳", layout="centered")

st.title("🌍 Smart Travel Planner")

# --- Number of travelers ---
st.subheader("👥 Number of Travelers")
traveler_count = st.number_input("Select number of travelers", min_value=1, max_value=10, value=2, step=1)

# --- City input ---
st.subheader("🏙️ Destination")
city_name = st.text_input("Enter the city you want to visit", placeholder="e.g., Almaty, Dubai, Riyadh")

# --- Date range input for next year ---
st.subheader("📅 Stay Dates")
today = datetime.datetime.now()
next_year = today.year + 1
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

stay_dates = st.date_input(
    "Select your vacation for next year",
    (jan_1, datetime.date(next_year, 1, 7)),
    min_value=jan_1,
    max_value=dec_31,
    format="DD.MM.YYYY",
)

# --- Budget range ---
st.subheader("💰 Budget (SAR per night)")
budget = st.slider(
    "Select your budget range",
    min_value=100,
    max_value=2000,
    value=(250, 400),
    step=50,
)

# --- Travel preference text ---
st.subheader("✨ Describe Your Ideal Stay")
user_description = st.text_area(
    "What kind of experience are you looking for?",
    placeholder="Example: I want a relaxing stay with a nice pool, great breakfast, and close to the city center.",
    height=150,
)

# --- Search button ---
if st.button("🔍 Search Hotels"):
    if not city_name:
        st.warning("Please enter a city name.")
    else:
        user_text = (
            f"Book a stay in {city_name} for {traveler_count} travelers from "
            f"{stay_dates[0]} to {stay_dates[1]}, in price range of {budget[0]} to {budget[1]} SAR per night. "
            f"{user_description}"
        )

        st.info("Searching for the best hotels... please wait ⏳")

        start = time.perf_counter()
        TopHotels = run_hotels(user_text)
        elapsed = time.perf_counter() - start

        st.success(f"✅ Found results in {elapsed:.2f} seconds")

        if TopHotels:
            for i, hotel in enumerate(TopHotels, start=1):
                st.markdown(f"### 🏨 {i}. {hotel.get('name', 'Unknown Hotel')}")
                st.json(hotel)
                st.markdown("---")
        else:
            st.error("No hotels found that match your preferences or budget.")

