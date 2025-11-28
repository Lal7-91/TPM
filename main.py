import datetime
import streamlit as st
from streamlit_option_menu import option_menu
from Flights.travel_flights_pipeline import run_flights
from Activities.travel_things_pipeline import run_tripadvisor


def run_tripadvisor_search(destination, start_date, end_date, travelers_num, budget_min, budget_max, description,
                           flights_checked, hotels_checked, activities_checked, preferences):
    with st.container():
        st.subheader("Search Results")

        options = []
        if flights_checked:
            options.append("Flights")
        if hotels_checked:
            options.append("Hotels")
        if activities_checked:
            options.append("Activities")

        if options:
            choice = option_menu(None, options, orientation="horizontal")

            if choice == "Flights":
                st.write("### ✈️ Best Flights")
                st.write("(Connect Flights API here)")

            elif choice == "Hotels":
                st.write("### 🏨 Best Hotels")
                st.write("(Connect Hotels LLM here)")

            elif choice == "Activities":
                st.write("### 🎡 Activities")
                st.write("(Connect TripAdvisor API here)")

        else:
            st.info("Enable at least one category to see results.")

        st.write("### User Preferences for Experience")
        st.write(preferences)


def main():
    st.set_page_config(page_title="Travel Planner Mate", layout="centered", page_icon="✈️")

    st.title("✈️ Travel Planner — SWE Project UI")

    if "show_results" not in st.session_state:
        st.session_state.show_results = False

    if "pref_nature" not in st.session_state:
        st.session_state.pref_nature = 50  # Nature vs Human-built
    if "pref_historical" not in st.session_state:
        st.session_state.pref_historical = 50  # Historical vs Modern

    today = datetime.date.today()
    six_months = today + datetime.timedelta(days=30 * 6)
    default_start = today
    default_end = today + datetime.timedelta(days=7)

    # Top container: Inputs
    with st.container():
        st.subheader("Trip Inputs")
        st.markdown("Enter your trip details below.")

        col1, col2 = st.columns(2)

        # LEFT COLUMN
        with col1:
            departure = st.text_input("From (Departure Location)")
            date_range = st.date_input(
                "Select your trip dates",
                (default_start, default_end),
                min_value=today,
                max_value=six_months,
                format="DD.MM.YYYY",
            )

            if isinstance(date_range, tuple):
                start_date, end_date = date_range
            else:
                start_date = end_date = date_range

            travelers_num = st.number_input("Travelers Number:", min_value=1, value=1)

            flights_checked = st.checkbox("Include Flights", value=True, key="flights_checkbox")
            hotels_checked = st.checkbox("Include Hotels", value=True, key="hotels_checkbox")
            activities_checked = st.checkbox("Include Activities", value=True, key="activities_checkbox")

        # RIGHT COLUMN
        with col2:
            destination = st.text_input("Destination", placeholder="Riyadh, Jeddah, Dammam")
            budget_min = st.number_input("Stay Budget Min per Night", min_value=0, value=500)
            budget_max = st.number_input("Stay Budget Max per Night", min_value=0, value=2000)
            description = st.text_area("Stay Imagination (optional)")

    # Second container: Sliders row
    with st.container():
        st.subheader("Activities Preferences")

        col1, col2 = st.columns(2)

        with col1:
            # Slider 1: Nature vs Human-built
            nature = st.slider("Nature (Human-built = 100 - Nature)", 0, 100,
                st.session_state.pref_nature if "pref_nature" in st.session_state else 50)
            human_built = 100 - nature
            st.write(f"Human-built: {human_built}%, Nature: {nature}%")

        with col2:
            # Slider 2: Historical vs Modern
            historical = st.slider("Historical (Modern = 100 - Historical)", 0, 100,
                               st.session_state.pref_historical if "pref_historical" in st.session_state else 50)
            modern = 100 - historical
            st.write(f"Modern: {modern}%, Old/Historical: {historical}%")

        preferences = {
            "Nature": nature,
            "Human-built": human_built,
            "Historical": historical,
            "Modern": modern
        }

    st.write("-----------------------------")

    if st.button("Search", type="primary"):
        st.session_state.show_results = True
        st.session_state.last_search = {
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "travelers_num": travelers_num,
            "budget_min": budget_min,
            "budget_max": budget_max,
            "description": description,
            "flights_checked": flights_checked,
            "hotels_checked": hotels_checked,
            "activities_checked": activities_checked,
            "preferences": preferences,
        }

    if st.session_state.show_results and "last_search" in st.session_state:
        search = st.session_state.last_search
        run_tripadvisor_search(
            search["destination"],
            search["start_date"],
            search["end_date"],
            search["travelers_num"],
            search["budget_min"],
            search["budget_max"],
            search["description"],
            search["flights_checked"],
            search["hotels_checked"],
            search["activities_checked"],
            search["preferences"],
        )


if __name__ == "__main__":
    main()
