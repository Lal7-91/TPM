import datetime
import streamlit as st
from streamlit_option_menu import option_menu
from TPM_runner import run_TPM

# -------------------------------
# Initialize session state
# -------------------------------
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "last_search_results" not in st.session_state:
    st.session_state.last_search_results = {}
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# -------------------------------
# Page UI
# -------------------------------
st.set_page_config(page_title="Travel Planner Mate", layout="centered", page_icon="✈️")
st.title("✈️ Travel Planner — SWE Project UI")

today = datetime.date.today()
six_months = today + datetime.timedelta(days=30 * 6)
default_start = today
default_end = today + datetime.timedelta(days=7)

# -------------------------------
# Top container: Inputs
# -------------------------------
with st.container():
    st.subheader("Trip Inputs")

    col1, col2 = st.columns(2)

    with col1:
        departure = st.text_input("From (Departure Location)")
        date_range = st.date_input(
            "Select your trip dates",
            (default_start, default_end),
            min_value=today,
            max_value=six_months,
            format="DD.MM.YYYY"
        )
        if isinstance(date_range, tuple):
            start_date, end_date = date_range
        else:
            start_date = end_date = date_range

        travelers_num = st.number_input("Travelers Number:", min_value=1, value=1)
        flights_checked = st.checkbox("Include Flights", value=True)
        hotels_checked = st.checkbox("Include Hotels", value=True)
        activities_checked = st.checkbox("Include Activities", value=True)

    with col2:
        destination = st.text_input("Destination", placeholder="Riyadh, Jeddah, Dammam")
        budget_min = st.number_input("Stay Budget Min per Night", min_value=0, value=500)
        budget_max = st.number_input("Stay Budget Max per Night", min_value=0, value=2000)
        description = st.text_area("Stay Imagination (optional)")

# -------------------------------
# Second container: Sliders row
# -------------------------------
with st.container():
    st.subheader("Experience Preferences (Two Sliders)")
    col1, col2 = st.columns(2)

    with col1:
        nature = st.slider("Nature (Human-built = 100 - Nature)", 0, 100, 50)
        human_built = 100 - nature

    with col2:
        historical = st.slider("Historical (Modern = 100 - Historical)", 0, 100, 50)
        modern = 100 - historical

    preferences = {
        "Nature": nature,
        "Human-built": human_built,
        "Historical": historical,
        "Modern": modern
    }

# -------------------------------
# Search button
# -------------------------------
if st.button("Search", type="primary"):
    st.session_state.show_results = True

    # Run TPM pipelines
    with st.spinner("Running search..."):
        st.session_state.last_search_results = run_TPM(
            from_city=departure,
            to_city=destination,
            travelers=travelers_num,
            dates=f"{start_date} to {end_date}",
            stay_image=None,
            activities_percentages={
                "nature": nature,
                "old/historical": historical,
                "modern": modern
            },
            run_hotels_flag=hotels_checked,
            run_flights_flag=flights_checked,
            run_tripadvisor_flag=activities_checked,
            top_n_hotels=5,
            top_n_activities=5
        )

# -------------------------------
# Display results with horizontal menu
# -------------------------------
if st.session_state.show_results and st.session_state.last_search_results:

    # Build menu options dynamically based on results
    available_categories = [
        key.capitalize() for key, val in st.session_state.last_search_results.items() if val
    ]
    if available_categories:
        st.subheader("Search Results")
        selected = option_menu(
            menu_title=None,
            options=available_categories,
            default_index=0,
            orientation="horizontal"
        )

        # Save selected category in session_state
        st.session_state.selected_category = selected

        # Show JSON for selected category
        category_key = selected.lower()
        if category_key in st.session_state.last_search_results:
            st.json(st.session_state.last_search_results[category_key])
